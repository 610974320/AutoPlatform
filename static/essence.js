
//菜单隐藏展示
function show_hidden(hiden,btn) {
    var hidden = document.getElementById(hiden);
    var id = document.getElementById(btn);
    var flag = false;
    id.onclick = function () {
        if (!flag) {
            hidden.style.display = 'block';
            flag = true;
        } else {
            hidden.style.display = 'none';
            flag = false;
        }
    }
}

function myinformation(id,name) {
    //dom寻找“myDropdown”节点，判断其是否包含“show”这个css选择器，如果包含删除它，否则，添加它
    document.getElementById(id).classList.toggle("show");
    // 点击下拉菜单意外区域隐藏，e参数为window.onclick这个整个区域
    window.onclick = function (e) {
        //判断window窗口区域是否匹配到“name”选择器，如果匹配到，继续寻找“myDropdown”，判断
        //myDropdown包含“show”选择器，
        if (!e.target.matches(name)) {
            var myDropdown = document.getElementById(id);
            if (myDropdown.classList.contains('show')) {
                myDropdown.classList.remove('show');
            }
        }
    }
}

//提示信息函数
function tips(el,info){
    var tip = document.getElementById(el);
    var success_tip = document.getElementById('success_tip');
    var fail_tip = document.getElementById('fail_tip');
    if ( tip.id === 'setips'){
        success_tip.innerHTML = info;
    }else {
        fail_tip.innerHTML = info;
    }
    tip.style.display = 'block';
    setTimeout(function(){tip.style.display = "none";},1000);

}

/*获取列表数据*/
function all_list(url, json_data) {
    $.ajax({
        url: url,
        type: "post",
        async: false,
        header: {csrfmiddlewaretoken: '{{ csrf_token }}'},
        data: json_data,
        timeout: 3000,
        success: function (response){
            data = response;
        }
    });

    return data
}

/*数据插入列表公共方法*/
function get_row(row) {
    //行数据循环（获取一行里面的所有数据，及某个对象里面的数，拼接成行字符串）

    //定义行字符串
    var rows_tr = '<tr>\n'+'<td>'+row.id+'</td>\n'+'<td>'+row.project_name+'</td>\n'+'<td>'+ row.user_name+'</td>\n' + '<td> 2020-8-26 </td>\n'+ '<td>' + '<li class="edit" onclick="click_edit(' + JSON.stringify(row).replace(/"/g, '&quot;') + ')" id="edit_'+row.id+'">编辑</li>\n' + '<span style="margin: 0 4px"> | </span>\n' + '<li class="delete" id="delete_'+row.id+'">删除</li>' + '</td>\n' + '</tr>';
    return rows_tr;
}

function buildlist(data,elment) {
    $(document).ready(function() {
        var str = '';
        //行字符串拼接
        for (var j = 0; j < data.length; j++) {
            str += get_row(data[j]);
        }
        $(elment + " tr").remove();
        $(elment).append(str);
    })
}
//page('/platform/project_list/?page=1','#projectinfo','.pagination')
function page(url, table_element) {
    var content_info = all_list(url);
    buildlist(content_info.data, table_element);
}

function turn_page(page_no){
    //翻页函数
	var totalPage = 10;
	var totalRecords = null;

	//生成分页
	//有些参数是可选的，比如lang，若不传有默认值
	kkpager.generPageHtml({
        pno: page_no,
        //总页码
        total: totalPage,
        //总数据条数
        totalRecords: totalRecords,
        mode: 'click',//默认值是link，可选link或者click
        click: function (n) {
            this.selectPage(n);

            if (n === 1) {
                //原本是实现无刷新跳转，我这是根据自己需求做的有刷新时跳转
                //第一页写逻辑跳转
                // 如：window.location.href=......;
            } else {
                //除了第一页写逻辑跳转
            }
            return false;
        }
	})
}


function click_edit(row) {

    var edit_id = document.getElementById("edit_"+row.id);
    console.log(edit_id);
    var edit_project = document.getElementById("edit_project");
    edit_id.onclick = (function() {
        console.log(11111111111111);
        console.log(edit_project);
        if (edit_project.style.display === "none") {
        edit_project.style.display = "block"
        }else {
            edit_project.style.display = "none"
        }
    })();

    console.log(row.id)
}