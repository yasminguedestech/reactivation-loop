import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl; mpl.rcParams.update(mpl.rcParamsDefault)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import numpy as np, pandas as pd

BG='#08071a'; CARD='#100f2e'; BORDER='#2a2560'
PURPLE='#6366f1'; LAV='#a78bfa'; CYAN='#38bdf8'
PINK='#f472b6'; TEXT='#ede9ff'; MUTED='#8b7ec8'
GREEN='#34d399'; YELLOW='#fbbf24'

plt.rcParams.update({
    'figure.facecolor':BG,'axes.facecolor':CARD,'axes.edgecolor':BORDER,
    'axes.labelcolor':MUTED,'axes.titlecolor':TEXT,'axes.titlesize':13,
    'axes.labelsize':10,'axes.titlepad':14,'axes.spines.top':False,
    'axes.spines.right':False,'axes.grid':True,'grid.color':BORDER,
    'grid.linewidth':0.6,'xtick.color':MUTED,'ytick.color':MUTED,
    'text.color':TEXT,'font.family':'DejaVu Sans',
    'legend.facecolor':CARD,'legend.edgecolor':BORDER,'legend.labelcolor':TEXT,
})

np.random.seed(42); n=500
df=pd.DataFrame({'motorista_id':range(1,n+1),
    'perfil':np.random.choice(['Novo','Recorrente','Veterano'],n,p=[0.3,0.4,0.3]),
    'dias_inativo':np.random.randint(15,46,n),
    'contato_externo':np.random.choice([0,1],n,p=[0.5,0.5])})

def reativou(row):
    base=0.15
    if row['contato_externo']==1: base+=0.20
    if row['perfil']=='Veterano': base+=0.10
    elif row['perfil']=='Recorrente': base+=0.05
    if row['dias_inativo']<=20: base+=0.10
    return np.random.binomial(1,min(base,1))

df['reativou']=df.apply(reativou,axis=1)
df['janela']=pd.cut(df['dias_inativo'],bins=[14,20,30,45],labels=['7-20 dias','21-30 dias','31-45 dias'])
perfis=['Novo','Recorrente','Veterano']
janelas=['7-20 dias','21-30 dias','31-45 dias']

# ── GRAF 1: Dashboard principal 2x3 ────────────────────────────────
fig = plt.figure(figsize=(18,11))
fig.patch.set_facecolor(BG)
fig.suptitle('Reactivation Loop — Reengajamento de Motoristas via WhatsApp',
             fontsize=18, fontweight='bold', color=PINK, y=1.01)
gs = gridspec.GridSpec(2,3,figure=fig,hspace=0.45,wspace=0.38)

# 1a. Donut
ax0=fig.add_subplot(gs[0,0])
ax0.set_facecolor(CARD); ax0.axis('off')
total_c=df[df['contato_externo']==1]
reativados=total_c['reativou'].sum(); nao_reat=len(total_c)-reativados
taxa_geral=reativados/len(total_c)*100
wedges,_,autotexts=ax0.pie([reativados,nao_reat],labels=None,autopct='%1.1f%%',
    colors=[CYAN,PURPLE+'88'],startangle=90,pctdistance=0.72,
    wedgeprops=dict(edgecolor=BG,linewidth=4,width=0.52))
for at in autotexts:
    at.set_fontsize(13); at.set_fontweight('bold'); at.set_color(TEXT)
ax0.text(0,0.15,f'{taxa_geral:.0f}%',ha='center',va='center',fontsize=26,color=CYAN,fontweight='bold')
ax0.text(0,-0.18,'reativacao',ha='center',va='center',fontsize=10,color=MUTED)
ax0.legend(handles=[mpatches.Patch(facecolor=CYAN,label=f'Reativou ({reativados})'),
    mpatches.Patch(facecolor=PURPLE+'88',label=f'Nao reativou ({nao_reat})')],
    loc='lower center',bbox_to_anchor=(0.5,-0.12),ncol=1,fontsize=9,frameon=False)
ax0.set_title('Taxa de Reativacao\n(Grupo Contactado)',color=TEXT,fontsize=12)

# 1b. Barras impacto com delta
ax1=fig.add_subplot(gs[0,1])
ax1.set_facecolor(CARD)
taxa=df.groupby('contato_externo')['reativou'].mean()*100
bars=ax1.bar(['Sem contato','Com contato'],taxa.values,color=[PURPLE+'88',CYAN],width=0.5,edgecolor=BG,linewidth=2)
for bar,val in zip(bars,taxa.values):
    ax1.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.6,
             f'{val:.1f}%',ha='center',fontsize=13,fontweight='bold',color=TEXT)
delta=taxa[1]-taxa[0]
ax1.annotate(f'+{delta:.1f}pp',xy=(1,taxa[1]/2),fontsize=16,fontweight='bold',color=GREEN,ha='center',va='center',
    bbox=dict(boxstyle='round,pad=0.3',facecolor=CARD,edgecolor=GREEN,alpha=0.9))
ax1.set_ylabel('Taxa de Reativacao (%)'); ax1.set_title('Impacto do Contato Externo')
ax1.tick_params(axis='x',colors=TEXT,labelsize=11)
ax1.spines['bottom'].set_color(BORDER); ax1.spines['left'].set_color(BORDER)

# 1c. Heatmap perfil x janela
ax2=fig.add_subplot(gs[0,2])
ax2.set_facecolor(CARD)
matriz=np.zeros((3,3))
for i,p in enumerate(perfis):
    for j,jan in enumerate(janelas):
        sub=df[(df['perfil']==p)&(df['janela']==jan)&(df['contato_externo']==1)]
        matriz[i,j]=sub['reativou'].mean()*100 if len(sub)>0 else 0
cmap_h=LinearSegmentedColormap.from_list('hm',['#100f2e','#6366f1','#38bdf8','#34d399'])
im=ax2.imshow(matriz,cmap=cmap_h,aspect='auto',vmin=0,vmax=65)
ax2.set_xticks(range(3)); ax2.set_xticklabels(janelas,fontsize=9,color=MUTED,rotation=15)
ax2.set_yticks(range(3)); ax2.set_yticklabels(perfis,fontsize=10,color=TEXT)
for i in range(3):
    for j in range(3):
        ax2.text(j,i,f'{matriz[i,j]:.0f}%',ha='center',va='center',fontsize=12,fontweight='bold',color=TEXT)
cb=fig.colorbar(im,ax=ax2,shrink=0.8,pad=0.02)
cb.ax.tick_params(colors=MUTED,labelsize=8)
ax2.set_title('Heatmap: Perfil x Janela\n(Taxa de Reativacao %)',color=TEXT,fontsize=12)
ax2.grid(False)

# 1d. Barras horizontais janela
ax3=fig.add_subplot(gs[1,0])
ax3.set_facecolor(CARD)
ax3.grid(axis='x',color=BORDER,linewidth=0.6,linestyle='--'); ax3.grid(axis='y',visible=False)
tj=df[df['contato_externo']==1].groupby('janela',observed=True)['reativou'].mean()*100
cores_j=[CYAN if v==tj.max() else PURPLE+'99' for v in tj.values]
bars=ax3.barh(tj.index.tolist(),tj.values,color=cores_j,edgecolor=BG,linewidth=1,height=0.5)
for bar,val in zip(bars,tj.values):
    ax3.text(val+0.5,bar.get_y()+bar.get_height()/2,f'{val:.1f}%',
             va='center',fontsize=11,fontweight='bold',color=CYAN if val==tj.max() else TEXT)
ax3.set_xlabel('Taxa de Reativacao (%)')
ax3.set_title('Janela Ideal de Intervencao\n(Grupo Contactado)')
ax3.tick_params(axis='y',colors=TEXT,labelsize=11)
ax3.spines['bottom'].set_color(BORDER); ax3.spines['left'].set_color(BORDER)

# 1e. Barras agrupadas por perfil
ax4=fig.add_subplot(gs[1,1])
ax4.set_facecolor(CARD)
x=np.arange(3); w=0.35
for grp,cor,off in [('Sem contato',PURPLE+'88',-w/2),('Com contato',CYAN,w/2)]:
    flag=0 if grp=='Sem contato' else 1
    vals=[df[(df['perfil']==p)&(df['contato_externo']==flag)]['reativou'].mean()*100 for p in perfis]
    bars2=ax4.bar(x+off,vals,width=w,color=cor,edgecolor=BG,linewidth=1.5,label=grp)
    for bar in bars2:
        h=bar.get_height()
        ax4.text(bar.get_x()+bar.get_width()/2,h+0.5,f'{h:.0f}%',ha='center',fontsize=9,fontweight='bold',color=TEXT)
ax4.set_title('Reativacao por Perfil')
ax4.set_ylabel('Taxa de Reativacao (%)')
ax4.set_xticks(x); ax4.set_xticklabels(perfis,fontsize=11,color=TEXT)
ax4.set_ylim(0,75); ax4.legend(frameon=True,fontsize=9)
ax4.spines['bottom'].set_color(BORDER); ax4.spines['left'].set_color(BORDER)

# 1f. Funil de reativacao
ax5=fig.add_subplot(gs[1,2])
ax5.set_facecolor(CARD); ax5.axis('off')
etapas=['Motoristas\nInativos','Grupo\nContactado','Engajaram','Reativaram']
valores=[500,250,int(250*0.65),reativados]
cores_f=[PURPLE+'66',LAV,CYAN+'aa',CYAN]
widths=[0.70,0.58,0.44,0.30]
y_pos=[0.82,0.60,0.38,0.16]
for i,(etapa,val,cor,wf,yf) in enumerate(zip(etapas,valores,cores_f,widths,y_pos)):
    x0=(1-wf)/2
    rect=mpatches.FancyBboxPatch((x0,yf-0.08),wf,0.14,boxstyle='round,pad=0.01',
        facecolor=cor,edgecolor=BG,linewidth=2,transform=ax5.transAxes,clip_on=False)
    ax5.add_patch(rect)
    ax5.text(0.5,yf,etapa,ha='center',va='center',fontsize=9,color=TEXT,fontweight='bold',transform=ax5.transAxes)
    ax5.text(0.5,yf-0.052,str(val),ha='center',va='center',fontsize=11,
             color=CYAN if i==3 else TEXT,fontweight='bold',transform=ax5.transAxes)
    if i<3:
        pct=valores[i+1]/valores[i]*100
        ax5.text(0.86,(y_pos[i]+y_pos[i+1])/2,f'{pct:.0f}%',
                 ha='center',va='center',fontsize=9,color=MUTED,transform=ax5.transAxes)
ax5.set_title('Funil de Reativacao',color=TEXT,fontsize=12,pad=14)

plt.savefig('graf1_contactado_vs_controle.png',dpi=150,bbox_inches='tight',facecolor=BG)
plt.close(); print('graf1 salvo')

# ── GRAF 2: Segmentacao detalhada ──────────────────────────────────
fig,axs=plt.subplots(1,3,figsize=(18,6))
fig.patch.set_facecolor(BG)
fig.suptitle('Segmentacao Detalhada — Perfil, Distribuicao e Tendencia',fontsize=15,fontweight='bold',color=TEXT)

# 2a. Stacked 100%
ax=axs[0]; ax.set_facecolor(CARD)
resumo=df[df['contato_externo']==1].groupby('perfil')['reativou'].agg(['sum','count'])
resumo['pct_sim']=resumo['sum']/resumo['count']*100
resumo['pct_nao']=100-resumo['pct_sim']
resumo=resumo.loc[perfis]
x=np.arange(3)
ax.bar(x,resumo['pct_sim'].values,color=CYAN,edgecolor=BG,linewidth=1.5,label='Reativou',width=0.5)
ax.bar(x,resumo['pct_nao'].values,bottom=resumo['pct_sim'].values,color=PURPLE+'66',edgecolor=BG,linewidth=1.5,label='Nao reativou',width=0.5)
for i,(_,row) in enumerate(resumo.iterrows()):
    ax.text(i,row['pct_sim']/2,f'{row["pct_sim"]:.0f}%',ha='center',va='center',fontsize=13,fontweight='bold',color=BG)
    ax.text(i,row['pct_sim']+row['pct_nao']/2,f'{row["pct_nao"]:.0f}%',ha='center',va='center',fontsize=11,color=MUTED)
ax.set_xticks(x); ax.set_xticklabels(perfis,color=TEXT,fontsize=11)
ax.set_ylabel('Composicao (%)'); ax.set_title('Composicao 100%\npor Perfil (Grupo Contactado)')
ax.set_ylim(0,112); ax.legend(frameon=True,fontsize=9)
ax.spines['bottom'].set_color(BORDER); ax.spines['left'].set_color(BORDER)

# 2b. Boxplot dias inativos
ax=axs[1]; ax.set_facecolor(CARD)
grp_c=df[df['contato_externo']==1]
g_sim=grp_c[grp_c['reativou']==1]['dias_inativo'].values
g_nao=grp_c[grp_c['reativou']==0]['dias_inativo'].values
bp=ax.boxplot([g_sim,g_nao],patch_artist=True,widths=0.4,
    medianprops=dict(color=TEXT,linewidth=2.5),
    whiskerprops=dict(color=MUTED,linewidth=1.3),
    capprops=dict(color=MUTED,linewidth=1.3),
    flierprops=dict(marker='o',markerfacecolor=CARD,markeredgecolor=MUTED,markersize=4,alpha=0.5))
bp['boxes'][0].set_facecolor(CYAN+'55'); bp['boxes'][0].set_edgecolor(CYAN)
bp['boxes'][1].set_facecolor(PINK+'44'); bp['boxes'][1].set_edgecolor(PINK)
ax.set_xticks([1,2]); ax.set_xticklabels(['Reativou','Nao Reativou'],color=TEXT,fontsize=11)
med0=np.median(g_sim); med1=np.median(g_nao)
ax.text(1,med0+1.5,f'Med: {med0:.0f}d',ha='center',fontsize=10,color=CYAN,fontweight='bold')
ax.text(2,med1+1.5,f'Med: {med1:.0f}d',ha='center',fontsize=10,color=PINK,fontweight='bold')
ax.set_ylabel('Dias de Inatividade')
ax.set_title('Distribuicao de Dias Inativos\n(Reativou x Nao reativou)')
ax.spines['bottom'].set_color(BORDER); ax.spines['left'].set_color(BORDER)

# 2c. Linha acumulada
ax=axs[2]; ax.set_facecolor(CARD)
dias_range=list(range(15,46))
taxa_c=[df[(df['contato_externo']==1)&(df['dias_inativo']<=d)]['reativou'].mean()*100 for d in dias_range]
taxa_nc=[df[(df['contato_externo']==0)&(df['dias_inativo']<=d)]['reativou'].mean()*100 for d in dias_range]
ax.fill_between(dias_range,taxa_c,taxa_nc,alpha=0.15,color=CYAN)
ax.plot(dias_range,taxa_c,color=CYAN,linewidth=2.5,label='Com contato')
ax.plot(dias_range,taxa_nc,color=PINK,linewidth=2,linestyle='--',label='Sem contato')
ax.axvline(20,color=YELLOW,linewidth=1.5,linestyle=':',alpha=0.8,label='Dia 20')
ax.fill_betweenx([0,50],15,20,alpha=0.06,color=GREEN)
ax.text(17.5,44,'Janela\notima',ha='center',fontsize=9,color=GREEN,fontweight='bold')
ax.set_xlabel('Dias de Inatividade (acumulado)')
ax.set_ylabel('Taxa de Reativacao (%)')
ax.set_title('Taxa Acumulada de Reativacao\npor Dia de Inatividade')
ax.legend(frameon=True,fontsize=9); ax.set_xlim(15,45)
ax.spines['bottom'].set_color(BORDER); ax.spines['left'].set_color(BORDER)

plt.tight_layout(pad=2.5)
plt.savefig('graf2_reativacao_por_perfil.png',dpi=150,bbox_inches='tight',facecolor=BG)
plt.close(); print('graf2 salvo')

# ── GRAF 3: Janela + Delta ──────────────────────────────────────────
fig,axs=plt.subplots(1,3,figsize=(18,6))
fig.patch.set_facecolor(BG)
fig.suptitle('Analise da Janela de Intervencao e Impacto por Segmento',fontsize=15,fontweight='bold',color=TEXT)

ax=axs[0]; ax.set_facecolor(CARD)
tj=df[df['contato_externo']==1].groupby('janela',observed=True)['reativou'].mean()*100
tjc=df[df['contato_externo']==0].groupby('janela',observed=True)['reativou'].mean()*100
x=np.arange(3); w=0.35
b1=ax.bar(x-w/2,tjc.values,width=w,color=PURPLE+'88',edgecolor=BG,linewidth=1.5,label='Sem contato')
b2=ax.bar(x+w/2,tj.values,width=w,color=CYAN,edgecolor=BG,linewidth=1.5,label='Com contato')
for bars_g in [b1,b2]:
    for bar in bars_g:
        h=bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2,h+0.5,f'{h:.0f}%',ha='center',fontsize=10,fontweight='bold',color=TEXT)
ax.set_xticks(x); ax.set_xticklabels(tj.index.tolist(),color=TEXT,fontsize=11)
ax.set_ylabel('Taxa de Reativacao (%)'); ax.set_title('Reativacao por Janela\nContactado vs Controle')
ax.legend(frameon=True,fontsize=10); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_:f'{v:.0f}%'))
ax.spines['bottom'].set_color(BORDER); ax.spines['left'].set_color(BORDER)

ax=axs[1]; ax.set_facecolor(CARD)
delta_j=tj.values-tjc.values
bars=ax.bar(tj.index.tolist(),delta_j,color=GREEN,edgecolor=BG,linewidth=1.5,width=0.5)
for bar,val in zip(bars,delta_j):
    ax.text(bar.get_x()+bar.get_width()/2,val+0.3,f'+{val:.1f}pp',
            ha='center',fontsize=13,fontweight='bold',color=TEXT)
ax.axhline(0,color=MUTED,linewidth=1,alpha=0.5)
ax.set_ylabel('Ganho em pp'); ax.set_title('Ganho do Contato por Janela\n(Delta = Contactado - Controle)')
ax.tick_params(axis='x',colors=TEXT,labelsize=11)
ax.spines['bottom'].set_color(BORDER); ax.spines['left'].set_color(BORDER)

ax=axs[2]; ax.set_facecolor(CARD)
delta_perf=[]
for p in perfis:
    t_c=df[(df['perfil']==p)&(df['contato_externo']==1)]['reativou'].mean()*100
    t_nc=df[(df['perfil']==p)&(df['contato_externo']==0)]['reativou'].mean()*100
    delta_perf.append(t_c-t_nc)
bars=ax.bar(perfis,delta_perf,color=[CYAN,LAV,PINK],edgecolor=BG,linewidth=1.5,width=0.5)
for bar,val in zip(bars,delta_perf):
    ax.text(bar.get_x()+bar.get_width()/2,val+0.3,f'+{val:.1f}pp',
            ha='center',fontsize=13,fontweight='bold',color=TEXT)
ax.axhline(0,color=MUTED,linewidth=1,alpha=0.5)
ax.set_ylabel('Ganho em pp (Contactado - Controle)')
ax.set_title('Ganho do Contato por Perfil\n(Quem mais se beneficia?)')
ax.tick_params(axis='x',colors=TEXT,labelsize=11)
ax.spines['bottom'].set_color(BORDER); ax.spines['left'].set_color(BORDER)

plt.tight_layout(pad=2.5)
plt.savefig('graf3_janela_intervencao.png',dpi=150,bbox_inches='tight',facecolor=BG)
plt.close(); print('graf3 salvo - todos prontos!')
