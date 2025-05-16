
import streamlit as st
import pandas as pd

st.set_page_config(page_title="FollowCheck", layout="centered")
st.title("🔍 FollowCheck – Analisador de Seguidores no Instagram")

st.markdown("Faça upload de dois arquivos CSV com as listas de seguidores para comparar quem saiu, quem entrou e quem continua.")

col1, col2 = st.columns(2)
with col1:
    file_antigo = st.file_uploader("📦 Lista antiga", type=["csv"], key="lista_antiga")
with col2:
    file_novo = st.file_uploader("🆕 Lista nova", type=["csv"], key="lista_nova")

if file_antigo and file_novo:
    df_antigo = pd.read_csv(file_antigo)
    df_novo = pd.read_csv(file_novo)

    seguidores_antigos = set(df_antigo.iloc[:, 0].dropna().astype(str))
    seguidores_novos = set(df_novo.iloc[:, 0].dropna().astype(str))

    deixaram_de_seguir = sorted(seguidores_antigos - seguidores_novos)
    novos_seguidores = sorted(seguidores_novos - seguidores_antigos)
    mantidos = sorted(seguidores_novos & seguidores_antigos)

    st.subheader("📊 Resumo Geral")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total antigo", len(seguidores_antigos))
    col2.metric("Total novo", len(seguidores_novos))
    col3.metric("❌ Saíram", len(deixaram_de_seguir))
    col4.metric("✅ Entraram", len(novos_seguidores))

    st.subheader("👥 Seguidores mantidos")
    st.write(mantidos if mantidos else "Ninguém foi mantido.")

    st.subheader("📤 Novos seguidores")
    st.write(novos_seguidores if novos_seguidores else "Nenhum novo seguidor.")

    st.subheader("👋 Deixaram de seguir")
    st.write(deixaram_de_seguir if deixaram_de_seguir else "Ninguém deixou de seguir.")

    # Oferece CSV para download
    def gerar_csv(lista, nome):
        df = pd.DataFrame(lista, columns=["username"])
        return df.to_csv(index=False).encode("utf-8")

    st.download_button("⬇️ Baixar quem saiu", gerar_csv(deixaram_de_seguir, "saíram"), file_name="deixaram_de_seguir.csv")
    st.download_button("⬇️ Baixar novos", gerar_csv(novos_seguidores, "novos"), file_name="novos_seguidores.csv")
    st.download_button("⬇️ Baixar mantidos", gerar_csv(mantidos, "mantidos"), file_name="seguidores_mantidos.csv")
