import streamlit as st
from sklearn.cluster import KMeans
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import io

# Fungsi untuk ekstraksi warna dominan
def extract_colors(image, num_colors=5):
    img = cv2.resize(image, (150, 150))
    img = img.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors, n_init='auto', random_state=42)
    kmeans.fit(img)
    colors = kmeans.cluster_centers_.astype(int)
    return colors

# Fungsi tampilan warna dengan kotak besar
def display_color_palette(colors):
    st.markdown("## 🎨 Palet Warna Dominan")
    cols = st.columns(len(colors))
    hex_list = []
    for idx, col in enumerate(cols):
        rgb = tuple(colors[idx])
        hex_color = '#%02x%02x%02x' % rgb
        hex_list.append((rgb, hex_color))
        with col:
            st.markdown(
                f"""
                <div style="width:100%%; height:100px; border-radius:10px; background-color:{hex_color}; border:1px solid #ccc"></div>
                <div style="text-align:center; margin-top:5px; font-size:14px;">
                    <b>RGB:</b> {rgb}<br>
                    <b>HEX:</b> <code>{hex_color}</code>
                </div>
                """, unsafe_allow_html=True
            )
    return hex_list

# Fungsi buat file warna sebagai string
def generate_palette_text(color_list):
    text = "Dominant Colors:\n\n"
    for i, (rgb, hex_val) in enumerate(color_list):
        text += f"Color {i+1}:\n"
        text += f"  RGB : {rgb}\n"
        text += f"  HEX : {hex_val}\n\n"
    return text

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="🎨 Color Picker by K-Means", layout="centered")

# Judul dan deskripsi
st.title("🎨 Dominant Color Picker from Image")
st.markdown(
    "Upload gambar dan aplikasi akan menampilkan **5 warna dominan**."
)

# Upload gambar
uploaded_file = st.file_uploader("📁 Unggah Gambar", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Gambar yang Diupload", use_container_width=True)

    # Konversi ke OpenCV format
    img_np = np.array(image)
    if img_np.shape[2] == 4:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)

    with st.spinner("🔍 Mengekstrak warna dominan..."):
        colors = extract_colors(img_np, num_colors=5)
        color_list = display_color_palette(colors)

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        # Generate file untuk download
        file_text = generate_palette_text(color_list)
        file_bytes = io.BytesIO()
        file_bytes.write(file_text.encode('utf-8'))
        file_bytes.seek(0)

        st.download_button(
            label="⬇️ Download Warna (TXT)",
            data=file_bytes,
            file_name="warna_dominan.txt",
            mime="text/plain"
        )

else:
    st.info("Silakan unggah gambar terlebih dahulu untuk melihat hasil palet warna.")
