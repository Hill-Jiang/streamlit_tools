import streamlit as st
from timestamp_converter import TimestampConverterPage
from json_formatter import JsonFormatterPage
from qr_code_tool import QrCodeToolPage
from lan_device_scanner import LanDeviceScannerPage
from md5_calculator import Md5CalculatorPage
from base64_encoder_decoder import Base64EncoderDecoderPage
from note_bookmark import NoteBookmarkPage
from device_management_system import DeviceManagementSystemPage

PAGES = {
    "时间戳转化": TimestampConverterPage,
    "局域网设备扫描": LanDeviceScannerPage,
    "MD5计算": Md5CalculatorPage,
    "Base64编解码": Base64EncoderDecoderPage,
    "JSON格式化": JsonFormatterPage,
    "二维码工具": QrCodeToolPage,
    "笔记收藏夹": NoteBookmarkPage
}


def main():
    max_height_css = """
<style>
pre {
    max-height: 500px; /* 调整此值以设置您所需的代码块最大高度 */
    overflow-y: auto; /* 添加滚动条 */
}
</style>
"""
    st.set_page_config(page_title="工具库", layout="wide")
    st.markdown(max_height_css, unsafe_allow_html=True)

    st.sidebar.header("实用小工具 ^_^")
    selection = st.sidebar.radio("选择工具", list(PAGES.keys()))

    page = PAGES[selection]()
    page.display()


if __name__ == "__main__":
    main()
