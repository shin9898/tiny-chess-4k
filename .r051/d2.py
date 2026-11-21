import json,os,re,urllib.request as U
E=os.environ['MAKEFUN_ENV_URL']
def post(p,d):
 return json.load(U.urlopen(U.Request(E+p,json.dumps(d).encode(),{'content-type':'application/json'})))
# board: 120 chars, a8=21 h8=28 a1=91 h1=98, side to move uppercase, rotated 180 after every move
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0}
D={'P':(-10,-20,-11,-9),'N':(-21,-19,-12,-8,8,12,19,21),'B':(-11,-9,9,11),'R':(-10,10,-1,1)}
D['Q']=D['K']=D['B']+D['R']
RP=re.compile('[PNBRQK]').finditer
KP=[15]*120;KP[91]=14;KP[98]=13;KP[21]=11;KP[28]=7
RV=[(c&1)<<3|(c&2)<<1|(c&4)>>1|(c&8)>>3 for c in range(16)]
MATE=99999
def tab(ph,b):
 # piece-square tables (material included) for the side whose pieces are uppercase in b,
 # specialised to b's pawn structure and king squares; ph: 24 opening .. 0 endgame
 OP=[0]*10;EP=[-1]*10
 for i,p in enumerate(b):
  if p=='P':OP[i%10]+=1
  if p=='p':EP[i%10]=max(EP[i%10],9-i//10)
 k=b.find('K');kf=k%10;kr=9-k//10;e=b.find('k');ef=e%10;er=9-e//10
 T={}
 for p in V:
  t=[0]*120
  for i in range(21,99):
   f=i%10;r=9-i//10
   if f<1 or f>8:continue
   x=abs(2*f-9);c=x+abs(2*r-7);cf=7-x;a=r-1;dk=max(abs(f-ef),abs(r-er))
   if p=='P':
    m=a*(3+cf)-(12 if r==1 and cf==6 else 0)+(kr<1 and abs(f-kf)<2 and 0<r-kr<3)*(14-4*(r-kr));e=10+6*a
    if r>=max(EP[f-1:f+2]):m+=a*a*2+5*a;e+=a*a*6+5*a
    if OP[f-1]+OP[f+1]<1:m-=10;e-=10
    if OP[f]>1:m-=8;e-=8
   elif p=='N':m=-3*c-(10 if r==0 else 0)+(7-dk)*3;e=-3*c
   elif p=='B':m=-2*c-(10 if r==0 else 0);e=-2*c
   elif p=='R':
    m=(20 if r==6 else 0)+(5 if cf>=4 else 0)+(7-dk)*2;e=(15 if r==6 else 0)
    if OP[f]<1:m+=10+10*(EP[f]<0);e+=10
   elif p=='Q':m=-c+(7-dk)*4;e=-2*c
   else:m=(r==0)*(15,25,0,5)[x//2]-25*r;e=40-6*c+(7-dk)*3
   t[i]=V[p]+(m*ph+e*(24-ph))//24
  T[p]=t
 return T
def att(b,k,u):
 # is square k attacked by side u (1: uppercase, 0: lowercase)
 P,N,B,R,Q,K='PNBRQK' if u else 'pnbrqk'
 for d in(-10,10,-1,1,-11,-9,9,11):
  j=k+d;q=b[j]
  if q==K:return 1
  while q=='.':j+=d;q=b[j]
  if q==Q or q==(R if d in(-10,10,-1,1) else B):return 1
 for d in D['N']:
  if b[k+d]==N:return 1
 return b[k+11]==P or b[k+9]==P if u else b[k-11]==P or b[k-9]==P
def gen(S,qs=0):
 # pseudo-legal moves (i,j,promo); qs: captures and queen promotions only
 b,c,ep=S[0],S[2],S[3];o=[];a=o.append;L='pnbrqk'
 for x in RP(b):
  i=x.start();p=b[i]
  if p=='P':
   j=i-10
   if b[j]=='.':
    if j<29:a((i,j,'Q'));qs or a((i,j,'N'))
    elif not qs:
     a((i,j,''))
     if i>80 and b[j-10]=='.':a((i,j-10,''))
   for j in(i-11,i-9):
    if b[j]in L or j==ep:
     if j<29:a((i,j,'Q'));qs or a((i,j,'N'))
     else:a((i,j,''))
  elif p=='N'or p=='K':
   for d in D[p]:
    q=b[i+d]
    if q in L or q=='.'and not qs:a((i,i+d,''))
   if p=='K'and c&3 and not qs:
    for r,w in((91,1),(98,2)):
     d=1 if r>i else -1
     if c&w and all(b[k]=='.'for k in range(i+d,r,d))and not att(b,i,0)and not att(b,i+d,0):a((i,i+2*d,''))
  else:
   for d in D[p]:
    j=i+d;q=b[j]
    while q=='.':
     qs or a((i,j,''));j+=d;q=b[j]
    if q in L:a((i,j,''))
 return o
def dl(S,m):
 b,ep,z=S[0],S[3],S[4];i,j,pr=m;p=b[i];q=b[j];A=TS[z];B=TS[1-z]
 v=A[pr or p][j]-A[p][i]
 if q!='.':
  v+=B[q.upper()][119-j]
  if q=='b'and b.count('b')==2:v+=30
 if p=='K'and abs(j-i)==2:r=98 if j>i else 91;v+=A['R'][(i+j)//2]-A['R'][r]
 if p=='P'and j==ep:v+=B['P'][109-j]
 return v
def mk(S,m):
 b,s,c,ep,z=S;i,j,pr=m;p=b[i];P=pr or p;ne=0
 s+=dl(S,m)
 if i<j:b=b[:i]+'.'+b[i+1:j]+P+b[j+1:]
 else:b=b[:j]+P+b[j+1:i]+'.'+b[i+1:]
 c&=KP[i]&KP[j]
 if p=='K':
  c&=12
  if abs(j-i)==2:r=98 if j>i else 91;k=(i+j)//2;b=b[:r]+'.'+b[r+1:];b=b[:k]+'R'+b[k+1:]
 elif p=='P':
  if j==ep:k=j+10;b=b[:k]+'.'+b[k+1:]
  if j==i-20:ne=129-i
 return(b[::-1].swapcase(),-s,RV[c],ne,1-z)
def nul(S):
 b,s,c,ep,z=S
 return(b[::-1].swapcase(),-s,RV[c],0,1-z)
def Q(S,a,bt):
 global NN
 NN+=1
 b,s=S[0],S[1]
 if att(b,b.find('k'),1):return MATE
 s+=4*(len(gen(S))-len(gen(nul(S))))
 if s>=bt:return s
 if s>a:a=s
 best=s
 ms=sorted([(dl(S,m),m) for m in gen(S,1)],reverse=True)
 for v,m in ms:
  if s+v+200<a:break
  v=-Q(mk(S,m),-bt,-a)
  if v>best:
   best=v
   if v>a:
    a=v
    if v>=bt:break
 return best
def srch(S,d,a,bt,ply,nm=1):
 global NN,BM
 NN+=1
 if NN>HARD:raise TimeoutError
 b,s=S[0],S[1]
 if att(b,b.find('k'),1):return MATE
 if ply and b in H:return -CT if ply%2==0 else CT
 chk=att(b,b.find('K'),0)
 if chk and ply<2*RD:d+=1
 if d<=0:return Q(S,a,bt)
 t=TT.get(S)
 if t and ply and t[0]>=d:
  tv=t[1]
  if t[2]==0 or(t[2]==1 and tv>=bt)or(t[2]==2 and tv<=a):return tv
 pv=bt-a>1
 if not chk and ply and not pv:
  if d<=3 and s-90*d>=bt:return s
  if nm and d>=2 and s>=bt and any(c in b for c in'NBRQ'):
   H.add(b)
   v=-srch(nul(S),d-3-(d>6),-bt,-bt+1,ply+1,0)
   H.discard(b)
   if v>=bt:return v
 tm=t[3] if t else None
 ks=KL[ply]
 ms=[]
 for m in gen(S):
  v=dl(S,m)
  ms.append((v+(99999 if m==tm else 5000 if b[m[1]]!='.'and v>-50 else 4000 if m in ks else HI.get((b[m[0]],m[1]),0)),v,m))
 ms.sort(reverse=True)
 best=-MATE;bm=None;a0=a;n=0;fp=0
 H.add(b)
 for k,v,m in ms:
  quiet=b[m[1]]=='.' and not m[2]
  if n and quiet and not chk and d<=2 and not pv and s+v+120*d<=a and m!=tm and m not in ks:
   fp=1;continue
  C=mk(S,m)
  if n==0:v=-srch(C,d-1,-bt,-a,ply+1)
  else:
   r=1 if d>=3 and n>=3 and quiet and not chk and m not in ks else 0
   if r and n>=8 and d>=5:r=2
   v=-srch(C,d-1-r,-a-1,-a,ply+1)
   if v>a and(r or v<bt):v=-srch(C,d-1,-bt,-a,ply+1)
  n+=1
  if v>best:
   best=v;bm=m
   if v>a:
    a=v
    if v>=bt:
     if quiet:
      if m not in ks:KL[ply]=[m,ks[0] if ks else None]
      x=(b[m[0]],m[1]);HI[x]=min(HI.get(x,0)+d*d,3000)
     break
 H.discard(b)
 if best==-MATE:best=a if fp else -MATE+ply if chk else 0
 TT[S]=(d,best,1 if best>=bt else 2 if best<=a0 else 0,bm)
 if ply==0:BM=bm
 return best
def sq(n,c):
 i=91+ord(n[0])-97-10*(int(n[1])-1)
 return 119-i if c else i
def nm(i,c):
 if c:i=119-i
 return chr(i%10+96)+str(10-i//10)
def think(g):
 global TS,H,NN,HARD,BM,KL,DEP,RD
 fen=g['start_fen'].split()[0]
 for k in'2345678':fen=fen.replace(k,'.'*int(k))
 for k in'1/':fen=fen.replace(k,'.' if k=='1' else '  ')
 b=' '*21+fen+' '*21
 S=(b,0,15,0,0);c=0;H=set();TS=[tab(24,b)]*2
 for u in g['moves']:
  H.add(S[0]);S=mk(S,(sq(u[:2],c),sq(u[2:4],c),u[4:].upper()));c^=1
 return root(S,c,g['legal_moves'])
def root(S,c,lg):
 global TS,NN,HARD,BM,KL,DEP,RD
 b=S[0]
 ph=min(24,sum((0,1,1,2,4)['PNBRQ'.index(x)] for x in b.upper() if x in'NBRQ'))
 TS=[tab(ph,b),tab(ph,b[::-1].swapcase())]
 s=30*((b.count('B')>1)-(b.count('b')>1))
 for i,p in enumerate(b):
  if p.isupper():s+=TS[0][p][i]
  elif p.islower():s-=TS[1][p.upper()][119-i]
 S=(b,s,S[2],S[3],0)
 if len(lg)==1:return lg[0]
 NN=0;HARD=BUD*2;KL=[[] for _ in range(200)];BM=None;best=None;HI.clear()
 try:
  for d in range(1,60):
   RD=d;v=srch(S,d,-MATE,MATE,0);DEP=d
   if BM:best=BM
   if NN>BUD*.4 or abs(v)>MATE-99:break
 except TimeoutError:pass
 if len(TT)>300000:TT.clear()
 u=best and nm(best[0],c)+nm(best[1],c)+best[2].lower()
 return u if u in lg else lg[0]
TT={};HI={};BUD=30000;CT=20
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':
  u=think(g)
  g=post('/move',{'game':g['game'],'move':u})
