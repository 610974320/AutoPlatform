from Share.ReadYaml import ReadConfig


class Paging:
    def __init__(self, current_page, total_count, url_address):
        """
        :param current_page: 当前显示页
        :param total_count:  总共条数
        :param url_address:  url地址
        :param pieces_page:   页面展示条数
        :param max_page:     页面最多展示多少页，多余的用“....”代替
        """
        self.total_count = total_count              #获取数据总共有多少条件数据
        self.url_address = url_address              #url地址，哪个接口地址
        self.current_page = current_page            #访问的当前是哪一页
        self.max_page = ReadConfig("max_page").base_config      #
        self.pieces_page = ReadConfig("pieces_page").base_config
        self.total_page, self.surplus = divmod(self.total_count, self.pieces_page)
        if self.surplus:
            self.total_page += 1

        try:
            self.page_num = int(self.current_page)
            # 如果输入的页码数超过了最大的页码数，默认返回最后一页
            if self.page_num > self.total_page:
                self.page_num = self.total_page
        except Exception as e:
            # 当输入的页码不是正经数字的时候 默认返回第一页的数据
            self.page_num = 1

        # 定义两个变量保存数据从哪儿取到哪儿
        self.data_start = (self.page_num - 1) * 10
        self.data_end = self.page_num * 10

        # 页面上总共展示多少页码
        if self.total_page < self.max_page:
            self.max_page = self.total_page

        half_max_page = self.max_page // 2
        # 页面上展示的页码从哪儿开始
        page_start = self.page_num - half_max_page
        # 页面上展示的页码到哪儿结束
        page_end = self.page_num + half_max_page
        # 如果当前页减一半 比1还小
        if page_start <= 1:
            page_start = 1
            page_end = self.max_page
        # 如果 当前页 加 一半 比总页码数还大
        if page_end >= self.total_page:
            page_end = self.total_page
            page_start = self.total_page - self.max_page + 1
        self.page_start = page_start
        self.page_end = page_end

    @property
    def start(self):
        return self.data_start

    @property
    def end(self):
        return self.data_end

    def page_html(self):
        # 自己拼接分页的HTML代码
        html_str_list = []
        # 加上第一页
        html_str_list.append('''<li onclick="page('{}?page=1','#projectinfow','.pagination')">首页</li>'''.format(self.url_address))

        # 判断一下 如果是第一页，就没有上一页
        if self.page_num <= 1:
            html_str_list.append('''<li onclick="page('{}?page=1','#projectinfow','.pagination')">&laquo;</li>'''.format(self.url_address))
        else:
            # 加一个上一页的标签
            html_str_list.append('''<li onclick="page('{0}?page={1}','#projectinfow','.pagination')">&laquo;</li>'''.format( self.url_address, self.page_num-1))

        for i in range(self.page_start, self.page_end+1):
            # 如果是当前页就加一个active样式类
            if i == self.page_num:
                tmp = '''<li onclick="page('{0}?page={1}','#projectinfow','.pagination')">{1}</li>'''.format(self.url_address, i)
            else:
                tmp = '''<li onclick="page('{0}?page={1}','#projectinfow','.pagination')">{1}</li>'''.format(self.url_address, i)

            html_str_list.append(tmp)

        # 加一个下一页的按钮
        # 判断，如果是最后一页，就没有下一页
        if self.page_num >= self.total_page:
            html_str_list.append('''<li class="disabled">&raquo</li>''')
        else:
            html_str_list.append('''<li onclick="page('{}?page={}','#projectinfow','.pagination')">&raquo;</li>'''.format( self.url_address, self.page_num+1))
        # 加最后一页
        html_str_list.append('''<li onclick="page('{}?page={}','#projectinfow','.pagination')">尾页</li>'''.format(self.url_address, self.total_page))
        page_html = "".join(html_str_list)
        return page_html