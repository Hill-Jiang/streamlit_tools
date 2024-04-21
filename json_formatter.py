import json
import subprocess
import streamlit as st


class JsonFormatterPage:
    def display(self):
        st.title("JSON格式化")
        cols = st.columns(2)
        with cols[0]:
            json_data = st.text_area("JSON数据", height=500)
            formatted_json = self.format_json(json_data)
            button = st.button("格式化")
        with cols[1]:
            if button:
                if formatted_json:
                    st.text("格式化结果:")
                    st.code(formatted_json, language="json")
                else:
                    st.text("请输入JSON数据")

        if button and formatted_json:
            # 展示PlantUML图
            uml_code = "@startjson\n" + formatted_json + "\n@endjson"
            # 将源码写入临时文件（确保清理临时文件）
            with open("./resources/temp.uml", "w") as f:
                f.write(uml_code)
            # 使用本地plantuml命令行工具生成图片（假设已经安装并添加到PATH）
            subprocess.run(["python", "-m", "plantuml", "./resources/temp.uml"])
            # 在Streamlit页面上显示图片
            st.image("./resources/temp.png")

    @staticmethod
    def format_json(data):
        """
        格式化json字符串，按照4个空格缩进
        :param data: str类型的json数据
        :return formatted_text: 格式化后的json数据，str类型
        """
        try:
            text = json.loads(data)
            formatted_text = json.dumps(text, ensure_ascii=False, indent=4)
        except Exception as e:
            formatted_text = "格式化失败: {}".format(e)
        return formatted_text
