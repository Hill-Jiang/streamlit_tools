import pandas as pd
import streamlit as st
from scapy.all import srp, Ether, ARP


class LanDeviceScannerPage:
    def display(self):
        cols = st.columns([1, 3, 1])
        with cols[1]:
            st.title("局域网设备扫描")
            st.text_input("请输入局域网网段", value='192.168.1.0/24', key="ip_range")
            st.text_input("请输入网卡名称", value='LAN', key="iface")
            button = st.button("开始扫描")
            if button:
                result = self.scan_device(st.session_state.ip_range, st.session_state.iface)
                if isinstance(result, dict):
                    st.write("扫描结果:")
                    df = pd.DataFrame.from_dict(result, orient='index', columns=['MAC'])
                    df.index.name = 'IP'
                    st.dataframe(df)
                else:
                    st.error(result)

    @staticmethod
    def scan_device(ip_range='192.168.1.0/24', iface='LAN'):
        """
        扫描局域网下的所有设备信息
        :param ip_range: 网段, ex 192.168.1.0/24
        :param iface: 网卡名称
        :return: 扫描到的设备IP和MAC
        """
        try:
            packet = Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip_range)
            ans, _ = srp(packet, timeout=2, iface=iface)
            result = {}
            for _, rcv in ans:
                result.update({rcv[ARP].psrc: rcv.src.upper()})
            return result
        except Exception as e:
            return f"Error: {e}"
