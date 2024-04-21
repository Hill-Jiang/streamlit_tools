import qrcode
import zxing
import streamlit as st


class QrCodeToolPage:
    def display(self):
        st.title("二维码工具")
        cols = st.columns(2)
        with cols[0]:
            st.subheader("生成二维码")
            string = st.text_input("请输入要生成二维码的字符串")
            if st.button("生成"):
                if string:
                    img_path = self.gen_qrcode(string)
                    st.success("二维码生成成功")
                    st.image(img_path)
                else:
                    st.error("请输入要生成二维码的字符串")
        with cols[1]:
            st.subheader("解析二维码")
            img_path = st.file_uploader("请上传要解析的二维码图片", type=["png", "jpg", "jpeg"])
            if img_path:
                img_path.seek(0)
                save_img_path = "./resources/upload_qrcode_img.png"
                with open(save_img_path, "wb") as f:
                    f.write(img_path.read())
                barcode = self.decode_qrcode(save_img_path)
                if barcode:
                    st.success("二维码解析成功")
                    st.write("解析结果")
                    st.code(barcode)
                else:
                    st.error("二维码解析失败")

    @staticmethod
    def gen_qrcode(string):
        img = qrcode.make(string)
        img.save("./resources/qrcode.png")
        return "./resources/qrcode.png"

    @staticmethod
    def decode_qrcode(filename="./resources/upload_qrcode_img.png"):
        reader = zxing.BarCodeReader()
        barcode = reader.decode(filename)
        return barcode.parsed
