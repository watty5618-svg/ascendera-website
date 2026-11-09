"""Offline validation for this buildless multilingual website: python scripts/check-site.py."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, struct, xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.tags=[];self.ids=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append((tag,a))
        if 'id' in a:self.ids.append(a['id'])

pages={p:Page(p.read_text(encoding='utf-8')) for p in root.rglob('*.html')}
errors=[];links=0
for p,parsed in pages.items():
    path=p.relative_to(root).as_posix(); ar=path.startswith('ar/');zh=path.startswith('zh/')
    html_tag=next(a for tag,a in parsed.tags if tag=='html')
    if html_tag.get('lang')!=('ar' if ar else 'zh-Hans' if zh else 'en'):errors.append(f'{path}: incorrect language')
    if ar and html_tag.get('dir')!='rtl':errors.append(f'{path}: missing RTL')
    if len(parsed.ids)!=len(set(parsed.ids)):errors.append(f'{path}: duplicate IDs')
    for tag,a in parsed.tags:
        references=[a.get(attr,'') for attr in ('href','src','poster')]
        references.extend(v.strip('\"\'') for v in re.findall(r'url\(([^)]+)\)',a.get('style','')))
        for raw in references:
            u=urlsplit(raw)
            if not raw or u.scheme or u.netloc:continue
            target=(root/unquote(u.path.lstrip('/'))) if u.path.startswith('/') else p.parent/unquote(u.path)
            if not u.path:target=p
            if target.is_dir():target=target/'index.html'
            target=target.resolve();links+=1
            if not target.is_file():errors.append(f'{path}: missing {raw}')
            elif u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{path}: missing anchor {raw}')
        if tag=='img' and 'alt' not in a:errors.append(f'{path}: image missing alternative text')
    if p.name!='404.html':
        alternates={a.get('hreflang') for t,a in parsed.tags if t=='link' and a.get('rel')=='alternate'}
        if alternates!={'en','ar','zh-Hans','x-default'}:errors.append(f'{path}: language alternates missing')
        if 'primary-navigation' not in parsed.ids:errors.append(f'{path}: navigation missing')
        switches={a.get('lang') for t,a in parsed.tags if t=='a' and 'lang-toggle' in a.get('class','').split()}
        expected={'en','ar','zh-Hans'}-{html_tag['lang']}
        if switches!=expected:errors.append(f'{path}: language switch missing')

def boxes(data,start=0,end=None):
    end=len(data) if end is None else end
    while start+8<=end:
        size,kind=struct.unpack_from('>I4s',data,start);header=8
        if size==1:size=struct.unpack_from('>Q',data,start+8)[0];header=16
        if size==0:size=end-start
        assert size>=header and start+size<=end
        yield kind,start+header,start+size
        start+=size
def duration(p):
    data=p.read_bytes()
    top=list(boxes(data));kinds=[b[0] for b in top]
    assert kinds.index(b'moov')<kinds.index(b'mdat'),f'{p}: no fast start'
    for k,s,e in top:
        if k!=b'moov':continue
        for kind,a,b in boxes(data,s,e):
            if kind==b'mvhd':
                if data[a]==0:scale,ticks=struct.unpack_from('>II',data,a+12)
                else:scale=struct.unpack_from('>I',data,a+20)[0];ticks=struct.unpack_from('>Q',data,a+24)[0]
                return ticks/scale
def seconds(t):
    parts=list(map(float,t.split(':')))
    return sum(v*60**i for i,v in enumerate(reversed(parts)))
catalog=json.loads((root/'assets/video/catalogue.json').read_text(encoding='utf-8'))
for film in catalog:
    if set(film['editions'])!={'en','ar','zh'}:errors.append(f'{film["id"]}: missing language edition')
    for lang,e in film['editions'].items():
        try:
            length=duration(root/e['movie'])
            assert abs(length-e['seconds'])<.25,'duration mismatch'
            captions=(root/e['vtt']).read_text(encoding='utf-8-sig')
            assert captions.startswith('WEBVTT'),'missing VTT header'
            cues=re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})',captions)
            assert cues,'no captions'
            previous=0
            for start,end in cues:
                a,b=seconds(start),seconds(end)
                assert a>=previous-.05 and b>a and b<=length+.5,'invalid caption timing'
                previous=b
            assert length-previous<5,'captions end too early'
            assert (root/e['transcript']).stat().st_size>100,'empty transcript'
            watch=root/(lang+'/' if lang in ('ar','zh') else '')/'veriso/watch'/film['id']/'index.html'
            parsed=pages[watch]
            player=next(a for t,a in parsed.tags if t=='video')
            assert 'controls' in player and 'autoplay' not in player and player.get('preload')=='none'
            track=next(a for t,a in parsed.tags if t=='track')
            assert track['srclang']==('zh-Hans' if lang=='zh' else lang)
            assert (watch.parent/track['src']).resolve()==(root/e['vtt']).resolve(),'wrong caption file'
            assert (watch.parent/player['poster']).resolve()==(root/e['poster']).resolve(),'wrong poster'
            assert any((watch.parent/a.get('src','')).resolve()==(root/e['movie']).resolve() for t,a in parsed.tags if t=='source'),'wrong video source'
            schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',watch.read_text(encoding='utf-8'),re.S).group(1))
            assert schema['inLanguage']==('zh-Hans' if lang=='zh' else lang) and schema['@type']=='VideoObject'
            assert schema['contentUrl']=='https://www.ascenderagroup.sa/'+e['movie'],'wrong schema movie'
            assert abs(float(schema['duration'][2:-1])-length)<.25,'schema duration mismatch'
            assert schema['transcript']==(root/e['transcript']).read_text(encoding='utf-8-sig').strip(),'stale transcript in schema'
        except Exception as ex:errors.append(f'{film["id"]}/{lang}: {ex}')
practice=json.loads((root/'assets/video/practice.json').read_text(encoding='utf-8'))
for film in practice:
    if set(film['editions'])!={'en','ar','zh'}:errors.append(f'{film["id"]}: missing practice language edition')
    for lang,edition in film['editions'].items():
        try:
            length=duration(root/edition['movie'])
            assert abs(length-edition['seconds'])<.25,'duration mismatch'
            captions=(root/edition['vtt']).read_text(encoding='utf-8-sig')
            assert captions.startswith('WEBVTT'),'missing caption header'
            cues=re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})',captions)
            assert cues,'missing captions'
            previous=0
            for start,end in cues:
                a,b=seconds(start),seconds(end)
                assert a>=previous-.05 and b>a and b<=length+.5,'invalid practice caption timing'
                previous=b
            assert length-previous<5,'practice captions end too early'
            transcript=(root/edition['transcript']).read_text(encoding='utf-8-sig').strip()
            assert len(transcript)>100,'missing transcript'
            page=root/(lang+'/' if lang in ('ar','zh') else '')/film['page']
            parsed=pages[page]
            player=next(a for t,a in parsed.tags if t=='video' and a.get('class')=='film-player')
            assert 'controls' in player and 'autoplay' not in player and player.get('preload')=='none'
            track=next(a for t,a in parsed.tags if t=='track')
            assert track['srclang']==edition['language']==('zh-Hans' if lang=='zh' else lang),'incorrect practice caption language'
            assert (page.parent/track['src']).resolve()==(root/edition['vtt']).resolve(),'wrong caption file'
            assert (page.parent/player['poster']).resolve()==(root/edition['poster']).resolve(),'wrong poster'
            assert any((page.parent/a.get('src','')).resolve()==(root/edition['movie']).resolve() for t,a in parsed.tags if t=='source'),'wrong video source'
            schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',page.read_text(encoding='utf-8'),re.S).group(1))
            assert schema['inLanguage']==('zh-Hans' if lang=='zh' else lang) and schema['@type']=='VideoObject'
            assert schema['contentUrl']=='https://www.ascenderagroup.sa/'+edition['movie']
            assert abs(float(schema['duration'][2:-1])-length)<.25,'schema duration mismatch'
            assert schema['transcript']==transcript,'stale transcript in schema'
            assert schema['uploadDate']==edition['uploadDate'],'publication date mismatch'
        except Exception as ex:errors.append(f'{film["id"]}/{lang}: {ex}')

tree=ET.parse(root/'sitemap.xml')
urls=[e.text for e in tree.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls)==len(set(urls))==len([p for p in pages if p.name!='404.html']),'Sitemap mismatch'
result={'htmlPages':len(pages),'localLinks':links,'productFilms':len(catalog),'practiceEditions':sum(len(f['editions']) for f in practice),'videoEditions':sum(len(f['editions']) for f in catalog+practice),'sitemapUrls':len(urls),'errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
