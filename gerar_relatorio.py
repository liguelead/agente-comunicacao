#!/usr/bin/env python3
"""
Gerador de Relatório PDF — Agente de Comunicação LigueLead
Uso: python3 gerar_relatorio.py --campanha "Nome" --periodo-inicio "DD/MM/AAAA" --periodo-fim "DD/MM/AAAA" --dados '{...}'
"""
import argparse
import json
import sys
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
except ImportError:
    print("Instale o reportlab: pip install reportlab")
    sys.exit(1)

# Cores LigueLead
TEAL    = colors.HexColor('#1BCCAE')
TEAL_DK = colors.HexColor('#0F7A68')
TEAL_LT = colors.HexColor('#E8FAF7')
BLACK   = colors.HexColor('#111111')
DARK    = colors.HexColor('#222222')
GRAY    = colors.HexColor('#666666')
GRAY_LT = colors.HexColor('#F4F4F4')
GRAY_BD = colors.HexColor('#E0E0E0')
WHITE   = colors.white
RED     = colors.HexColor('#D93636')

W, H = A4


def S(name, **kw):
    return ParagraphStyle(name, **kw)


def gerar(campanha, periodo_inicio, periodo_fim, dados, saida=None):
    agora = datetime.now().strftime('%d/%m/%Y às %H:%M')
    nome_arquivo = saida or f"relatorio-{campanha.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}.pdf"

    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=A4,
        leftMargin=14*mm, rightMargin=14*mm,
        topMargin=14*mm, bottomMargin=14*mm,
    )
    col_w = W - 28*mm
    story = []

    # Estilos
    S_hdr   = S('hdr',  fontName='Helvetica-Bold', fontSize=8,  textColor=WHITE,  leading=11, alignment=TA_CENTER)
    S_cell  = S('cell', fontName='Helvetica',      fontSize=8,  textColor=DARK,   leading=11)
    S_bold  = S('bold', fontName='Helvetica-Bold', fontSize=8,  textColor=DARK,   leading=11)
    S_teal  = S('teal', fontName='Helvetica-Bold', fontSize=8,  textColor=TEAL_DK,leading=11)
    S_red   = S('red',  fontName='Helvetica',      fontSize=8,  textColor=RED,    leading=11)
    S_gray  = S('gray', fontName='Helvetica',      fontSize=8,  textColor=GRAY,   leading=11)
    S_kv    = S('kv',   fontName='Helvetica-Bold', fontSize=20, textColor=DARK,   leading=24, alignment=TA_CENTER)
    S_ktl   = S('ktl',  fontName='Helvetica-Bold', fontSize=20, textColor=TEAL_DK,leading=24, alignment=TA_CENTER)
    S_kl    = S('kl',   fontName='Helvetica-Bold', fontSize=7,  textColor=GRAY,   leading=10, alignment=TA_CENTER)
    S_ks    = S('ks',   fontName='Helvetica',      fontSize=7,  textColor=GRAY,   leading=10, alignment=TA_CENTER)
    S_obs   = S('obs',  fontName='Helvetica',      fontSize=8,  textColor=DARK,   leading=13)
    S_ftr   = S('ftr',  fontName='Helvetica',      fontSize=7,  textColor=GRAY,   alignment=TA_CENTER, leading=11)
    S_meta  = S('meta', fontName='Helvetica',      fontSize=8,  textColor=GRAY,   leading=12)
    S_metab = S('metb', fontName='Helvetica-Bold', fontSize=8,  textColor=DARK,   leading=12)
    S_sec   = S('sec',  fontName='Helvetica-Bold', fontSize=8,  textColor=TEAL_DK,leading=12, spaceAfter=3)

    def tbl_style(extra=None):
        base = [
            ('GRID', (0,0), (-1,-1), 0.5, GRAY_BD),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
        ]
        return TableStyle(base + (extra or []))

    # ── Cabeçalho ─────────────────────────────────────────────────
    hdr_data = [[
        Paragraph('<font color="#1BCCAE"><b>Ligue</b></font><font color="#111111"><b>Lead</b></font>',
                  S('logo', fontName='Helvetica-Bold', fontSize=20, textColor=DARK, leading=24)),
        Paragraph(
            f'<b>RELATÓRIO DE PERFORMANCE</b><br/>'
            f'<font size="8" color="#666666">Agente de Comunicação · Campanha: {campanha}</font>',
            S('hr2', fontName='Helvetica-Bold', fontSize=12, textColor=DARK, leading=18, alignment=TA_RIGHT)),
    ]]
    ht = Table(hdr_data, colWidths=[col_w*0.4, col_w*0.6])
    ht.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'BOTTOM'),('LEFTPADDING',(0,0),(-1,-1),0),
                             ('RIGHTPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(ht)
    story.append(HRFlowable(width='100%', thickness=2, color=TEAL, spaceAfter=6))

    # Meta
    meta_data = [[
        Paragraph('Período', S_meta),
        Paragraph(f'<b>{periodo_inicio} – {periodo_fim}</b>', S_metab),
        Paragraph('Estratégia', S_meta),
        Paragraph(f'<b>{dados.get("regua", "[Régua]")}</b>', S_metab),
        Paragraph('Gerado em', S_meta),
        Paragraph(f'<b>{agora}</b>', S_metab),
    ]]
    mt = Table(meta_data, colWidths=[col_w*0.1, col_w*0.23, col_w*0.1, col_w*0.23, col_w*0.1, col_w*0.24])
    mt.setStyle(tbl_style([('BACKGROUND',(0,0),(-1,-1),GRAY_LT)]))
    story.append(mt)
    story.append(Spacer(1, 10))

    # ── KPIs ──────────────────────────────────────────────────────
    sms   = dados.get('sms',   {})
    flash = dados.get('flash', {})
    voz   = dados.get('voz',   {})

    total_env  = sms.get('enviados',0) + flash.get('enviados',0) + voz.get('realizadas',0)
    total_ent  = sms.get('entregues',0) + flash.get('entregues',0)
    total_ate  = voz.get('atendidas',0)
    taxa_ent   = f"{total_ent/max(sms.get('enviados',0)+flash.get('enviados',0),1)*100:.1f}%" if total_env else '—'
    taxa_ate   = f"{total_ate/max(voz.get('realizadas',0),1)*100:.1f}%" if voz.get('realizadas') else '—'

    story.append(Paragraph('RESUMO EXECUTIVO', S_sec))
    kpi_data = [
        [Paragraph('TOTAL ENVIADOS', S_kl), Paragraph('ENTREGUES', S_kl),
         Paragraph('TAXA DE ENTREGA', S_kl), Paragraph('ATENDIDAS (VOZ)', S_kl),
         Paragraph('TAXA DE ATENDIMENTO', S_kl)],
        [Paragraph(f'{total_env:,}', S_kv), Paragraph(f'{total_ent:,}', S_kv),
         Paragraph(taxa_ent, S_ktl), Paragraph(f'{total_ate:,}', S_kv),
         Paragraph(taxa_ate, S_ktl)],
        [Paragraph('SMS + Flash + Voz', S_ks), Paragraph('Confirmado pela operadora', S_ks),
         Paragraph('Meta ≥ 85%', S_ks), Paragraph(f'De {voz.get("realizadas",0):,} realizadas', S_ks),
         Paragraph('Meta ≥ 70%', S_ks)],
    ]
    kt = Table(kpi_data, colWidths=[col_w/5]*5, rowHeights=[12, 28, 11])
    kt.setStyle(tbl_style([
        ('BACKGROUND',(0,0),(-1,0),GRAY_LT),
        ('LINEABOVE',(0,0),(-1,0),2,TEAL),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    story.append(kt)
    story.append(Spacer(1, 12))

    # ── Performance por dia ────────────────────────────────────────
    por_dia = dados.get('por_dia', [])
    if por_dia:
        story.append(Paragraph('PERFORMANCE POR DIA E CANAL', S_sec))
        day_rows = [[Paragraph(h, S_hdr) for h in
                     ['Data', 'Canal', 'Enviados', 'Entregues / Atendidas', 'Falhas', 'Inválidos', 'Taxa']]]
        for i, r in enumerate(por_dia):
            bg = WHITE if i % 2 == 0 else GRAY_LT
            day_rows.append([
                Paragraph(r.get('data',''), S_cell),
                Paragraph(r.get('canal',''), S_cell),
                Paragraph(str(r.get('enviados','')), S_cell),
                Paragraph(str(r.get('entregues','')), S_cell),
                Paragraph(str(r.get('falhas','')), S_red if r.get('falhas',0)>0 else S_cell),
                Paragraph(str(r.get('invalidos','—')), S_cell),
                Paragraph(f'<font color="#1BCCAE"><b>{r.get("taxa","")}</b></font>', S_cell),
            ])
        # linha de total
        day_rows.append([
            Paragraph('<b>TOTAL</b>', S_teal), Paragraph('', S_cell),
            Paragraph(f'<b>{total_env:,}</b>', S_bold),
            Paragraph(f'<b>{total_ent+total_ate:,}</b>', S_bold),
            Paragraph(f'<b>{sms.get("falhas",0)+flash.get("falhas",0)+voz.get("falhas",0)}</b>', S_bold),
            Paragraph(f'<b>{sms.get("invalidos",0)+flash.get("invalidos",0)}</b>', S_bold),
            Paragraph(f'<b><font color="#1BCCAE">{taxa_ent}</font></b>', S_bold),
        ])
        dt = Table(day_rows, colWidths=[col_w*0.11, col_w*0.13, col_w*0.12, col_w*0.22, col_w*0.12, col_w*0.12, col_w*0.18])
        dt.setStyle(tbl_style([
            ('BACKGROUND',(0,0),(-1,0),TEAL_DK),
            ('BACKGROUND',(0,-1),(-1,-1),TEAL_LT),
            ('LINEABOVE',(0,-1),(-1,-1),1,TEAL),
        ]))
        story.append(dt)
        story.append(Spacer(1, 12))

    # ── Detalhe por canal ──────────────────────────────────────────
    story.append(Paragraph('DETALHE POR CANAL', S_sec))
    canais_rows = [[Paragraph(h, S_hdr) for h in
                    ['Canal', 'Enviados', 'Entregues / Atendidas', 'Falhas', 'Inválidos', 'Taxa']]]
    for canal, d in [('SMS', sms), ('SMS Flash', flash)]:
        env = d.get('enviados',0)
        ent = d.get('entregues',0)
        fal = d.get('falhas',0)
        inv = d.get('invalidos',0)
        tx  = f"{ent/max(env,1)*100:.1f}%" if env else '—'
        canais_rows.append([
            Paragraph(canal, S_cell), Paragraph(f'{env:,}', S_cell),
            Paragraph(f'{ent:,}', S_cell),
            Paragraph(f'{fal:,}', S_red if fal>0 else S_cell),
            Paragraph(f'{inv:,}', S_cell),
            Paragraph(f'<font color="#1BCCAE"><b>{tx}</b></font>', S_cell),
        ])
    v = voz
    env_v = v.get('realizadas',0)
    ate_v = v.get('atendidas',0)
    fal_v = v.get('falhas',0)
    tx_v  = f"{ate_v/max(env_v,1)*100:.1f}%" if env_v else '—'
    canais_rows.append([
        Paragraph('Voz', S_cell), Paragraph(f'{env_v:,}', S_cell),
        Paragraph(f'{ate_v:,}', S_cell),
        Paragraph(f'{fal_v:,}', S_red if fal_v>0 else S_cell),
        Paragraph('—', S_cell),
        Paragraph(f'<font color="#1BCCAE"><b>{tx_v}</b></font>', S_cell),
    ])
    canais_rows.append([
        Paragraph('<b>Total</b>', S_teal),
        Paragraph(f'<b>{total_env:,}</b>', S_bold),
        Paragraph(f'<b>{total_ent+total_ate:,}</b>', S_bold),
        Paragraph(f'<b>{sms.get("falhas",0)+flash.get("falhas",0)+fal_v}</b>', S_bold),
        Paragraph(f'<b>{sms.get("invalidos",0)+flash.get("invalidos",0)}</b>', S_bold),
        Paragraph(f'<b><font color="#1BCCAE">{taxa_ent}</font></b>', S_bold),
    ])
    ct = Table(canais_rows, colWidths=[col_w*0.15, col_w*0.13, col_w*0.25, col_w*0.13, col_w*0.13, col_w*0.21])
    ct.setStyle(tbl_style([
        ('BACKGROUND',(0,0),(-1,0),TEAL_DK),
        ('ROWBACKGROUNDS',(0,1),(-1,-2),[WHITE,GRAY_LT]),
        ('BACKGROUND',(0,-1),(-1,-1),TEAL_LT),
        ('LINEABOVE',(0,-1),(-1,-1),1,TEAL),
    ]))
    story.append(ct)
    story.append(Spacer(1, 12))

    # ── Observações ────────────────────────────────────────────────
    obs = dados.get('observacoes', [])
    if obs:
        story.append(Paragraph('OBSERVAÇÕES DO AGENTE', S_sec))
        obs_text = '<br/>'.join(f'• {o}' for o in obs)
        obs_tbl = Table([[Paragraph(obs_text, S_obs)]], colWidths=[col_w])
        obs_tbl.setStyle(tbl_style([
            ('BACKGROUND',(0,0),(-1,-1),GRAY_LT),
            ('LEFTPADDING',(0,0),(-1,-1),12),
            ('LINEBEFORE',(0,0),(0,-1),3,TEAL),
            ('BOX',(0,0),(-1,-1),0.5,GRAY_BD),
        ]))
        story.append(obs_tbl)
        story.append(Spacer(1, 10))

    # Rodapé
    story.append(HRFlowable(width='100%', thickness=1, color=GRAY_BD, spaceBefore=4, spaceAfter=4))
    story.append(Paragraph(
        'Relatório gerado automaticamente pelo Agente de Comunicação LigueLead · liguelead.com.br',
        S_ftr))

    doc.build(story)
    return nome_arquivo


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--campanha', required=True)
    parser.add_argument('--periodo-inicio', required=True)
    parser.add_argument('--periodo-fim', required=True)
    parser.add_argument('--dados', required=True, help='JSON com sms, flash, voz, por_dia, observacoes')
    parser.add_argument('--saida', default=None)
    args = parser.parse_args()

    dados = json.loads(args.dados)
    arquivo = gerar(args.campanha, args.periodo_inicio, args.periodo_fim, dados, args.saida)
    print(f'✅ Relatório gerado: {arquivo}')
