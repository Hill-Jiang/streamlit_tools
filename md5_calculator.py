import hashlib
import streamlit as st


class Md5CalculatorPage:
    def display(self):
        cols = st.columns([1, 3, 1])
        with cols[1]:
            st.title("MD5计算")
            file = st.file_uploader("请选择文件")
            button = st.button("计算")
            if button:
                if file:
                    st.markdown("##### MD5值")
                    md5_data = self.md5_encrypt(file.read())
                    st.code(md5_data)
                else:
                    st.warning("请选择文件")

    @staticmethod
    def md5_encrypt(data):
        """
        计算文件的md5值
        :param data: 待计算的数据，str或bytes
        :return md5_data: md5计算结果
        """
        h = hashlib.md5()
        if isinstance(data, str):
            h.update(data.encode(encoding='utf-8'))
        else:
            h.update(data)
        return h.hexdigest().upper()