"""Offline validation for this buildless bilingual website: python scripts/check-site.py."""
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
    path=p.relative_to(root).as_posix(); ar=path.startswith('ar/')
    html_tag=next(a for tag,a in parsed.tags if tag=='html')
    if html_tag.get('lang')!=('ar' if ar else 'en'):errors.append(f'{path}: incorrect language')
    if ar and html_tag.get('dir')!='rtl':errors.append(f'{path}: missing RTL')
    if len(parsed.ids)!=len(set(parsed.ids)):errors.append(f'{path}: duplicate IDs')
    for tag,a in parsed.tags:
        for attr in ('href','src','poster'):
            raw=a.get(attr,''); u=urlsplit(raw)
            if not raw or u.scheme or u.netloc:continue
            target=(root/unquote(u.path.lstrip('/'))) if u.path.startswith('/') else p.parent/unquote(u.path)
            if not u.path:target=p
            if target.is_dir():target=target/'index.html'
            target=target.resolve();links+=1
            if not target.is_file():errors.append(f'{path}: missing {raw}')
            elif u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{path}: missing anchor {raw}')
        if tag=='img' and 'alt' not in a:errors.append(f'{path}: image missing alternative text')
    if p.name!='404.html':
        if len([a for t,a in parsed.tags if t=='link' and a.get('rel')=='alternate'])!=3:errors.append(f'{path}: language alternates missing')
        if 'primary-navigation' not in parsed.ids:errors.append(f'{path}: navigation missing')

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
            watch=root/('ar/' if lang=='ar' else '')/'veriso/watch'/film['id']/'index.html'
            parsed=pages[watch]
            player=next(a for t,a in parsed.tags if t=='video')
            assert 'controls' in player and 'autoplay' not in player and player.get('preload')=='none'
            track=next(a for t,a in parsed.tags if t=='track')
            assert track['srclang']==lang
            schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',watch.read_text(encoding='utf-8'),re.S).group(1))
            assert schema['inLanguage']==lang and schema['@type']=='VideoObject'
        except Exception as ex:errors.append(f'{film["id"]}/{lang}: {ex}')
practice=json.loads((root/'assets/video/practice.json').read_text(encoding='utf-8'))
try:
    length=duration(root/practice['movie'])
    assert abs(length-practice['seconds'])<.25,'duration mismatch'
    captions=(root/practice['vtt']).read_text(encoding='utf-8-sig')
    assert captions.startswith('WEBVTT'),'missing caption header'
    cues=re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})',captions)
    assert cues,'missing captions'
    previous=0
    for start,end in cues:
        a,b=seconds(start),seconds(end)
        assert a>=previous-.05 and b>a and b<=length+.5,'invalid practice caption timing'
        previous=b
    assert length-previous<5,'practice captions end too early'
    assert (root/practice['transcript']).stat().st_size>100,'missing transcript'
    for prefix in ('','ar/'):
        page=root/(prefix+'advisory/hsse/index.html')
        parsed=pages[page]
        player=next(a for t,a in parsed.tags if t=='video')
        assert 'controls' in player and 'autoplay' not in player and player.get('preload')=='none'
        track=next(a for t,a in parsed.tags if t=='track')
        assert track['srclang']==practice['language']=='en','incorrect practice caption language'
        schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',page.read_text(encoding='utf-8'),re.S).group(1))
        assert schema['inLanguage']=='en' and schema['@type']=='VideoObject'
except Exception as ex:errors.append(f'hsse-practice/en: {ex}')

tree=ET.parse(root/'sitemap.xml')
urls=[e.text for e in tree.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls)==len(set(urls))==len(pages)-1,'Sitemap mismatch'
result={'htmlPages':len(pages),'localLinks':links,'bilingualFilms':len(catalog),'practiceEditions':1,'videoEditions':sum(len(f['editions']) for f in catalog)+1,'sitemapUrls':len(urls),'errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
