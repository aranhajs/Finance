import streamlit as st
import yfinance as yf
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Valuation B3 - Graham & Bazin",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Calculadora de Valuation: Fórmula de Graham & Método de Bazin")
st.markdown("Selecione um ativo da B3 para calcular o preço justo, o preço teto e ver um diagnóstico consolidado.")

# Lista de ativos da B3 (Ações e FIIs) em ordem alfabética
tickers_b3 = sorted([
    'ABCB4.SA', 'ABEV3.SA', 'AGRO3.SA', 'ALPA4.SA', 'ALUP11.SA', 'AMAR3.SA', 
    'ANIM3.SA', 'ARZZ3.SA', 'ASAI3.SA', 'AZUL4.SA', 'B3SA3.SA', 'BBAS3.SA', 
    'BBDC3.SA', 'BBDC4.SA', 'BBSE3.SA', 'BEEF3.SA', 'BLAU3.SA', 'BMGB4.SA', 
    'BPAC11.SA', 'BPAN4.SA', 'BRAP4.SA', 'BRFS3.SA', 'BRKM5.SA', 'CASH3.SA', 
    'CCRO3.SA', 'CEAB3.SA', 'CIEL3.SA', 'CLSC4.SA', 'CMIG3.SA', 'CMIG4.SA', 
    'CMIN3.SA', 'COGN3.SA', 'CPFE3.SA', 'CPLE3.SA', 'CPLE6.SA', 'CRFB3.SA', 
    'CSAN3.SA', 'CSNA3.SA', 'CVCB3.SA', 'CYRE3.SA', 'DXCO3.SA', 'ECOR3.SA', 
    'EGIE3.SA', 'ELET3.SA', 'ELET6.SA', 'EMBR3.SA', 'ENBR3.SA', 'ENEV3.SA', 
    'ENGI11.SA', 'ENJU3.SA', 'EQTL3.SA', 'EZTC3.SA', 'FHER3.SA', 'FLRY3.SA', 
    'GGBR4.SA', 'GOAU4.SA', 'GOLL4.SA', 'GRND3.SA', 'HAPV3.SA', 'HYPE3.SA', 
    'IGTI11.SA', 'IRBR3.SA', 'ITSA3.SA', 'ITSA4.SA', 'ITUB3.SA', 'ITUB4.SA', 
    'JBSS3.SA', 'JHSF3.SA', 'JALL3.SA', 'KEPL3.SA', 'KLBN11.SA', 'LAVV3.SA', 
    'LIGT3.SA', 'LJQQ3.SA', 'LOGG3.SA', 'LREN3.SA', 'LWSA3.SA', 'MDIA3.SA', 
    'MEAL3.SA', 'MELK3.SA', 'MGLU3.SA', 'MLAS3.SA', 'MOAR3.SA', 'MRFG3.SA', 
    'MRVE3.SA', 'MULT3.SA', 'MYPK3.SA', 'NEOE3.SA', 'NTCO3.SA', 'ODPV3.SA', 
    'ONCO3.SA', 'OSFL3.SA', 'PCAR3.SA', 'PETR3.SA', 'PETR4.SA', 'PETZ3.SA', 
    'PINE4.SA', 'PLPL3.SA', 'POMO4.SA', 'POSI3.SA', 'PRIO3.SA', 'PRNR3.SA', 
    'PSSA3.SA', 'qual3.SA', 'RADL3.SA', 'RAIL3.SA', 'RAIZ4.SA', 'RANI3.SA', 
    'RAPT4.SA', 'RDOR3.SA', 'RECV3.SA', 'RENT3.SA', 'ROMI3.SA', 'RRRP3.SA', 
    'SANB11.SA', 'SANB3.SA', 'SANB4.SA', 'SBSP3.SA', 'SEQL3.SA', 'SLCE3.SA', 
    'SMTO3.SA', 'SULA11.SA', 'SUZB3.SA', 'TAEE11.SA', 'TASA4.SA', 'TCSA3.SA', 
    'TECN3.SA', 'TIMS3.SA', 'TOTS3.SA', 'TPIS3.SA', 'TRIS3.SA', 'UGPA3.SA', 
    'UNIP6.SA', 'USIM5.SA', 'VALE3.SA', 'VBBR3.SA', 'VIIA3.SA', 'VITT3.SA', 
    'VIVT3.SA', 'VLID3.SA', 'VULC3.SA', 'WEGE3.SA', 'WIZC3.SA', 'YDUQ3.SA',
    # FIIs Populares
    'AFHI11.SA', 'ALZR11.SA', 'ARRI11.SA', 'BARI11.SA', 'BBFO11.SA', 'BBIM11.SA', 
    'BCFF11.SA', 'BIME11.SA', 'BPFF11.SA', 'BRCO11.SA', 'BTLG11.SA', 'BTRA11.SA', 
    'BZLI11.SA', 'CARE11.SA', 'CPTS11.SA', 'CVBI11.SA', 'CXCE11.SA', 'DEVA11.SA', 
    'ERCR11.SA', 'EXRE11.SA', 'FAED11.SA', 'FCFL11.SA', 'FINC11.SA', 'FIIB11.SA', 
    'FIIP11.SA', 'FISD11.SA', 'FLMA11.SA', 'FPAB11.SA', 'GALG11.SA', 'GCRI11.SA', 
    'GGRC11.SA', 'HABT11.SA', 'HCTR11.SA', 'HFOF11.SA', 'HGLG11.SA', 'HGRU11.SA', 
    'HLOG11.SA', 'HSAF11.SA', 'HSLG11.SA', 'HSML11.SA', 'HTMX11.SA', 'IRDM11.SA', 
    'JBFO11.SA', 'JSRE11.SA', 'KFOF11.SA', 'KNCA11.SA', 'KNCR11.SA', 'KNHY11.SA', 
    'KNIP11.SA', 'KNRE11.SA', 'KNRI11.SA', 'KNSC11.SA', 'MALL11.SA', 'MCCI11.SA', 
    'MFII11.SA', 'MGFF11.SA', 'MXRF11.SA', 'OUJP11.SA', 'PATC11.SA', 'PORD11.SA', 
    'RBCR11.SA', 'RBFF11.SA', 'RBHY11.SA', 'RBRP11.SA', 'RBRR11.SA', 'RBRX11.SA', 
    'RBVA11.SA', 'RECR11.SA', 'RECT11.SA', 'RZAK11.SA', 'RZTR11.SA', 'SADI11.SA', 
    'SARE11.SA', 'SNCI11.SA', 'SNFF11.SA', 'SNAG11.SA', 'SPVJ11.SA', 'TEPP11.SA', 
    'TGAR11.SA', 'TRXF11.SA', 'URPR11.SA', 'VCJR11.SA', 'VGIA11.SA', 'VGIR11.SA', 
    'VIUR11.SA', 'VISC11.SA', 'VTLT11.SA', 'XPCA11.SA', 'XPML11.SA', 'RZAG11.SA', 
    'RZTR11.SA', 'HFOF11.SA', 'HGRU11.SA', 'HLOG11.SA', 'HSAF11.SA','GARE11.SA', 
    'GGRC11.SA', 'HCTR11.SA', 'HFOF11.SA', 'HGLG11.SA', 'HGRU11.SA',
])

# Layout em colunas
col1, col2 = st.columns([2, 1])

with col1:
    ticker_selecionado = st.selectbox(
        "Selecione o ativo da B3 (ou digite para buscar):",
        tickers_b3,
        index=tickers_b3.index('PETR4.SA') if 'PETR4.SA' in tickers_b3 else 0
    )

with col2:
    taxa_bazin_pct = st.slider(
        "Taxa de Retorno Alvo (Bazin % a.a.)",
        min_value=4.0, max_value=12.0, value=6.0, step=0.5
    )
    taxa_bazin = taxa_bazin_pct / 100.0

@st.cache_data(ttl=3600)
def carregar_dados_ativo(ticker):
    acao = yf.Ticker(ticker)
    info = acao.info
    # CORREÇÃO AQUI: Mudado de acao.dividendos para acao.dividends
    dividendos = acao.dividends
    return info, dividendos

if st.button("Analisar Ativo Selecionado", type="primary"):
    with st.spinner(f"Buscando dados em tempo real apenas para {ticker_selecionado}..."):
        try:
            info, dividendos = carregar_dados_ativo(ticker_selecionado)
            preco_atual = info.get('currentPrice') or info.get('regularMarketPrice')
            
            if not preco_atual:
                st.error("Não foi possível obter o preço atual do ativo. Verifique se o ticker está correto.")
            else:
                st.metric(label=f"Cotação Atual ({ticker_selecionado})", value=f"R$ {preco_atual:.2f}")
                
                col_g, col_b = st.columns(2)
                
                graham_valido = False
                aprovado_graham = False
                margem_graham = 0.0
                
                bazin_valido = False
                aprovado_bazin = False
                margem_bazin = 0.0

                # 1. FÓRMULA DE GRAHAM
                with col_g:
                    st.subheader("🛡️ Fórmula de Graham")
                    lpa = info.get('trailingEps')
                    vpa = info.get('bookValue')
                    
                    if lpa is not None and vpa is not None and lpa > 0 and vpa > 0:
                        graham_valido = True
                        preco_graham = (22.5 * lpa * vpa) ** 0.5
                        margem_graham = ((preco_graham - preco_atual) / preco_graham) * 100
                        aprovado_graham = preco_atual < preco_graham
                        
                        st.write(f"**LPA (Lucro por Ação):** R$ {lpa:.2f}")
                        st.write(f"**VPA (Valor Patrimonial):** R$ {vpa:.2f}")
                        st.metric(
                            "Preço Justo (Graham)", 
                            f"R$ {preco_graham:.2f}", 
                            delta=f"{margem_graham:.2f}% de margem"
                        )
                        
                        if aprovado_graham:
                            st.success(f"✅ O ativo está com **desconto** de {margem_graham:.1f}% segundo Graham.")
                        else:
                            st.warning(f"⚠️ O ativo está acima do preço justo (-{abs(margem_graham):.1f}%).")
                    else:
                        st.info("ℹ️ Dados de LPA/VPA indisponíveis (Comum em FIIs ou empresas com prejuízo).")

                # 2. MÉTODO DE BAZIN
                with col_b:
                    st.subheader("💰 Método de Bazin")
                    
                    if not dividendos.empty:
                        um_ano_atras = pd.Timestamp.now(tz=dividendos.index.tz) - pd.DateOffset(years=1)
                        divs_12m = dividendos[dividendos.index >= um_ano_atras]
                        total_div_12m = divs_12m.sum()
                        
                        if total_div_12m > 0:
                            bazin_valido = True
                            preco_teto_bazin = total_div_12m / taxa_bazin
                            margem_bazin = ((preco_teto_bazin - preco_atual) / preco_teto_bazin) * 100
                            aprovado_bazin = preco_atual < preco_teto_bazin
                            
                            st.write(f"**Dividendos (últimos 12m):** R$ {total_div_12m:.2f}")
                            st.write(f"**Taxa Alvo Configurada:** {taxa_bazin_pct}% a.a.")
                            st.metric(
                                "Preço Teto (Bazin)", 
                                f"R$ {preco_teto_bazin:.2f}", 
                                delta=f"{margem_bazin:.2f}% de margem"
                            )
                            
                            if aprovado_bazin:
                                st.success(f"✅ Abaixo do Preço Teto! Margem de {margem_bazin:.1f}%.")
                            else:
                                st.warning(f"⚠️ Acima do Preço Teto de Bazin (-{abs(margem_bazin):.1f}%).")
                        else:
                            st.info("ℹ️ O ativo não distribuiu dividendos nos últimos 12 meses.")
                    else:
                        st.info("ℹ️ Sem histórico recente de dividendos cadastrado.")

                # 3. DIAGNÓSTICO E DICA CONSOLIDADA
                st.divider()
                st.subheader("🎯 Diagnóstico Consolidado & Dica de Análise")
                
                is_fii = ticker_selecionado.endswith("11.SA")
                
                if is_fii and not graham_valido:
                    if bazin_valido and aprovado_bazin:
                        st.success(f"🟢 **Oportunidade de Renda (FII):** Como fundos imobiliários são avaliados pelo fluxo de proventos, **{ticker_selecionado}** está abaixo do Preço Teto de Bazin (margem de **{margem_bazin:.1f}%**). **Dica:** Verifique o P/VP e a vacância dos imóveis.")
                    elif bazin_valido and not aprovado_bazin:
                        st.warning(f"🟡 **Aguardar / Cautela (FII):** O FII está negociando acima do Preço Teto de Bazin para a meta de {taxa_bazin_pct}% a.a.")
                    else:
                        st.error(f"🔴 **Sem Dados Suficientes:** Não há histórico de proventos nos últimos 12 meses.")
                
                elif graham_valido and bazin_valido:
                    if aprovado_graham and aprovado_bazin:
                        st.success(f"🟢 **Forte Atratividade (Dupla Aprovação):** **{ticker_selecionado}** está barato tanto por Graham (**+{margem_graham:.1f}%**) quanto por Bazin (**+{margem_bazin:.1f}%**).")
                    elif aprovado_graham and not aprovado_bazin:
                        st.info(f"🔵 **Foco em Crescimento (Aprovado em Graham):** Negocia com desconto no valor intrínseco (**+{margem_graham:.1f}%**), mas paga dividendos abaixo da meta.")
                    elif not aprovado_graham and aprovado_bazin:
                        st.info(f"🔵 **Foco em Dividendos (Aprovado em Bazin):** O ativo está caro segundo Graham, mas entrega bom retorno em proventos.")
                    else:
                        st.error(f"🔴 **Caro nos Dois Métodos (Evitar Compra):** **{ticker_selecionado}** está acima do Preço Justo de Graham e do Preço Teto de Bazin.")
                
                elif graham_valido and not bazin_valido:
                    if aprovado_graham:
                        st.info(f"🔵 **Desconto Patrimonial (Sem Dividendos):** Negocia com **{margem_graham:.1f}%** de desconto em Graham (reinveste lucros).")
                    else:
                        st.warning(f"🟡 **Cautela:** Não paga dividendos recentes e negocia acima do preço justo.")
                
                else:
                    st.error(f"🔴 **Alerta Fundamentalista:** Ativo apresentou prejuízo acumulado e não pagou dividendos recentes.")

                st.caption("⚠️ *Nota: Esta ferramenta realiza cálculos matemáticos automáticos baseados em dados públicos e não constitui recomendação oficial de investimento.*")
                        
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o ativo: {e}")
