import base64
import streamlit as st


class Base64EncoderDecoderPage:
    def display(self):
        st.title("Base64编解码")
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Base64编码")
            plaintext = st.text_area("明文", "")
            button = st.button("编码")
            if button:
                ciphertext = self.base64_encode(plaintext)
                st.write("密文")
                st.code(ciphertext)
        with cols[1]:
            st.subheader("Base64解码")
            ciphertext = st.text_area("密文", "")
            button = st.button("解码")
            if button:
                plaintext = self.base64_decode(ciphertext)
                st.write("明文")
                st.code(plaintext)

    @staticmethod
    def base64_encode(plaintext):
        ciphertext = base64.b64encode(plaintext.encode())
        return ciphertext.decode()

    @staticmethod
    def base64_decode(ciphertext):
        plaintext = base64.b64decode(ciphertext).decode()
        return plaintext
