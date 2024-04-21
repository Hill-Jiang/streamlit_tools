import json
import os
import time
import streamlit as st
from streamlit import session_state as ss


class NoteBookmarkPage:
    def __init__(self, data_file="data.json"):
        self.data_file = data_file

        # 初始化数据文件（如果不存在）
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump({"groups": []}, f)

    def load_data(self):
        """
        加载数据
        :return: 数据
        """
        with open(self.data_file, "r") as f:
            return json.load(f)

    def save_data(self, data):
        """
        保存数据
        :param data: 数据
        :return:
        """
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def create_group(self, group_name):
        """
        创建分组
        :param group_name: 分组名称
        :return:
        """
        data = self.load_data()
        group_id = len(data["groups"]) + 1
        new_group = {"id": group_id, "name": group_name, "notes": []}
        data["groups"].append(new_group)
        self.save_data(data)

    def delete_group(self, group_id):
        """
        删除分组
        :param group_id: 分组ID
        :return:
        """
        data = self.load_data()
        group_index = next((i for i, g in enumerate(data["groups"]) if g["id"] == group_id), None)
        if group_index is not None:
            del data["groups"][group_index]
            self.save_data(data)

    def update_group_name(self, group_id, new_name):
        """
        更新分组名称
        :param group_id: 分组ID
        :param new_name: 新名称
        :return:
        """
        data = self.load_data()
        group_index = next((i for i, g in enumerate(data["groups"]) if g["id"] == group_id), None)
        if group_index is not None:
            data["groups"][group_index]["name"] = new_name
            self.save_data(data)

    def create_note(self, group_id, note_name, note_content):
        """
        创建笔记
        :param group_id: 分组ID
        :param note_name: 笔记名称
        :param note_content: 笔记内容
        :return:
        """
        data = self.load_data()
        group_index = next((i for i, g in enumerate(data["groups"]) if g["id"] == group_id), None)
        if group_index is not None:
            new_note = {"name": note_name, "content": note_content}
            data["groups"][group_index]["notes"].append(new_note)
            self.save_data(data)

    def update_note(self, group_id, note_index, new_name, new_content):
        """
        更新笔记
        :param group_id: 分组ID
        :param note_index: 笔记索引
        :param new_name: 新名称
        :param new_content: 新内容
        :return:
        """
        data = self.load_data()
        group_index = next((i for i, g in enumerate(data["groups"]) if g["id"] == group_id), None)
        if group_index is not None and 0 <= note_index < len(data["groups"][group_index]["notes"]):
            data["groups"][group_index]["notes"][note_index]["name"] = new_name
            data["groups"][group_index]["notes"][note_index]["content"] = new_content
            self.save_data(data)

    def delete_note(self, group_id, note_index):
        """
        删除笔记
        :param group_id: 分组ID
        :param note_index: 笔记索引
        :return:
        """
        data = self.load_data()
        group_index = next((i for i, g in enumerate(data["groups"]) if g["id"] == group_id), None)
        if group_index is not None and 0 <= note_index < len(data["groups"][group_index]["notes"]):
            del data["groups"][group_index]["notes"][note_index]
            self.save_data(data)

    def _create_group_form(self):
        """
        创建分组表单
        :return:
        """
        form_container = st.expander("创建分组", expanded=True)
        group_name = form_container.text_input("分组名称:")
        cols = st.columns(2)
        confirm_button = cols[0].button("确认")
        cancel_button = cols[1].button("取消")
        if confirm_button:
            if group_name:
                self.create_group(group_name)
                ss.creating_group = False
                st.success(f"分组 **{group_name}** 创建成功")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("请填写分组名称")
        if cancel_button:
            ss.creating_group = False
            st.rerun()

    def _delete_group_form(self, group_id):
        """
        删除分组表单
        :param group_id: 分组ID
        :return:
        """
        form_container = st.expander("删除分组", expanded=True)
        form_container.warning(f"确认要删除该分组吗？")
        cols = form_container.columns(10)
        confirm_button = cols[0].button("确认", type="primary")
        cancel_button = cols[1].button("取消")
        if confirm_button:
            self.delete_group(group_id)
            ss[f"delete_group_{group_id}"] = False
            st.success("已删除")
            time.sleep(1)
            st.rerun()
        elif cancel_button:
            ss[f"delete_group_{group_id}"] = False
            st.rerun()

    def _update_group_name_form(self, group_id):
        """
        修改分组名称表单
        :param group_id: 分组ID
        :return:
        """
        form_container = st.expander("修改分组名称", expanded=True)
        new_name = form_container.text_input("新名称:")
        cols = form_container.columns(10)
        confirm_button = cols[0].button("确认")
        cancel_button = cols[1].button("取消")
        if confirm_button:
            self.update_group_name(group_id, new_name)
            ss[f"rename_group_{group_id}"] = False
            st.success("已修改")
            time.sleep(1)
            st.rerun()
        elif cancel_button:
            ss[f"rename_group_{group_id}"] = False
            st.rerun()

    def _create_note_form(self, group_id):
        """
        创建笔记表单
        :param group_id: 分组ID
        :return:
        """
        form_container = st.expander("为该分组添加笔记", expanded=True)
        note_name = form_container.text_input("名称:")
        note_content = form_container.text_area("内容:")
        cols = form_container.columns(10)
        confirm_button = cols[0].button("确认")
        cancel_button = cols[1].button("取消")
        if confirm_button:
            if note_name and note_content:
                self.create_note(group_id, note_name, note_content)
                ss[f"creating_note_of_{group_id}"] = False
                st.success("已保存")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("请填写名称/内容")
        elif cancel_button:
            ss[f"creating_note_of_{group_id}"] = False
            st.rerun()

    def _update_note_form(self, group_id, note_index):
        """
        修改笔记表单
        :param group_id: 分组ID
        :param note_index: 笔记索引
        :return:
        """
        form_container = st.expander("修改笔记内容", expanded=True)
        note = self.load_data()["groups"][group_id - 1]["notes"][note_index]
        old_note_name = note["name"]
        new_note_name = form_container.text_input("名称:", value=old_note_name)
        new_note_content = form_container.text_area("内容:")
        cols = form_container.columns(10)
        confirm_button = cols[0].button("确认")
        cancel_button = cols[1].button("取消")
        if confirm_button:
            self.update_note(group_id, note_index, new_note_name, new_note_content)
            ss[f"update_note_{group_id}_{note_index}"] = False
            st.success("已保存")
            time.sleep(1)
            st.rerun()
        elif cancel_button:
            ss[f"update_note_{group_id}_{note_index}"] = False
            st.rerun()

    def _delete_note_form(self, group_id, note_index):
        """
        删除笔记表单
        :param group_id: 分组ID
        :param note_index: 笔记索引
        :return:
        """
        form_container = st.expander("删除笔记", expanded=True)
        form_container.warning(f"确认要删除该条笔记吗？")
        cols = form_container.columns(10)
        confirm_button = cols[0].button("确认", type="primary")
        cancel_button = cols[1].button("取消")
        if confirm_button:
            self.delete_note(group_id, note_index)
            ss[f"delete_note_{group_id}_{note_index}"] = False
            st.success("已删除")
            time.sleep(1)
            st.rerun()
        elif cancel_button:
            ss[f"delete_note_{group_id}_{note_index}"] = False
            st.rerun()

    def display_notes(self, group_id):
        """
        显示笔记
        :param group_id: 分组ID
        :return:
        """
        data = self.load_data()
        group = next((g for g in data["groups"] if g["id"] == group_id), None)
        if group is not None:
            for i, note in enumerate(group["notes"]):
                st.markdown(f"**{note['name']}**")
                note_cols = st.columns([7, 1])
                with note_cols[0]:
                    st.code(note["content"])
                with note_cols[1]:
                    # 修改笔记
                    if f"update_note_{group_id}_{i}" not in ss:
                        ss[f"update_note_{group_id}_{i}"] = False
                    if st.button("修改笔记", key=f"update_note_button_{group_id}_{i}"):
                        ss[f"update_note_{group_id}_{i}"] = True
                    # 删除笔记
                    if f"delete_note_{group_id}_{i}" not in ss:
                        ss[f"delete_note_{group_id}_{i}"] = False
                    if st.button(":red[删除笔记]", key=f"delete_note_button_{group_id}_{i}"):
                        ss[f"delete_note_{group_id}_{i}"] = True
                if ss[f"update_note_{group_id}_{i}"]:
                    self._update_note_form(group_id, i)
                if ss[f"delete_note_{group_id}_{i}"]:
                    self._delete_note_form(group_id, i)

    def display(self):
        """
        显示页面
        :return:
        """
        st.title("笔记收藏夹")
        data = self.load_data()
        cols = st.columns([1, 5])
        # 分组导航栏
        with cols[0]:
            group_name_list = [group["name"] for group in data["groups"]]
            selection = st.radio("选择分组", group_name_list)
            # 新建分组
            if "creating_group" not in ss:
                ss.creating_group = False
            if st.button("创建新分组"):
                ss.creating_group = True
            if ss.creating_group:
                self._create_group_form()
        with cols[1]:
            # 显示所选分组及其笔记内容
            for group in data["groups"]:
                if group["name"] == selection:
                    st.subheader(group["name"])
                    group_cols = st.columns(6)
                    group_id = group["id"]
                    with group_cols[0]:
                        # 重命名分组
                        if f"rename_group_{group_id}" not in ss:
                            ss[f"rename_group_{group_id}"] = False
                        if st.button("重命名分组"):
                            ss[f"rename_group_{group_id}"] = True
                    with group_cols[1]:
                        # 删除分组
                        if f"delete_group_{group_id}" not in ss:
                            ss[f"delete_group_{group_id}"] = False
                        if st.button(":red[删除分组]"):
                            ss[f"delete_group_{group_id}"] = True
                    with group_cols[2]:
                        # 为该分组新建笔记
                        if f"creating_note_of_{group_id}" not in ss:
                            ss[f"creating_note_of_{group_id}"] = False
                        if st.button(":green[为分组添加笔记]"):
                            ss[f"creating_note_of_{group_id}"] = True
                    if ss[f"rename_group_{group_id}"]:
                        self._update_group_name_form(group_id)
                    if ss[f"delete_group_{group_id}"]:
                        self._delete_group_form(group_id)
                    if ss[f"creating_note_of_{group_id}"]:
                        self._create_note_form(group_id)
                    # 显示该分组下的笔记内容
                    self.display_notes(group_id)
