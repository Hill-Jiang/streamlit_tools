import time
import streamlit as st


class TimestampConverterPage:
    def display(self):
        cols = st.columns([1, 3, 1])
        with cols[1]:
            st.title("时间戳转化")
            st.header("时间戳转时间")
            timestamp = st.text_input("10位/13位时间戳")
            process_button = st.button("转换")
            if process_button:
                if timestamp:
                    real_time = self.time2timestamp(timestamp)
                    st.markdown(f"##### 时间: {real_time}")
                else:
                    st.markdown("##### 请输入时间戳")
            st.divider()
            now = self.get_current_timestamp()
            st.markdown(f"##### 当前时间: {self.time2timestamp(now)}")
            st.markdown(f"##### 当前时间戳: {now}")

    @staticmethod
    def time2timestamp(timestamp):
        """
        将10位/13位时间戳转化为时间
        :param timestamp: 10位/13位时间戳，str类型
        :return time: %Y-%m-%d %H:%M:%S格式的时间，str类型
        """
        timestamp = str(timestamp)
        if len(timestamp) == 10:
            timestamp = int(timestamp)
        elif len(timestamp) == 13:
            timestamp = int(timestamp) // 1000
        else:
            return "时间戳长度错误"
        real_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        return real_time

    @staticmethod
    def get_current_timestamp():
        """
        获取当前时间戳
        :return timestamp: 当前时间戳，10位，str类型
        """
        timestamp = int(time.time())
        return str(timestamp)
