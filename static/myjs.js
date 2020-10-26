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

function menu(id) {
    document.getElementById(id).classList.toggle("show");
}

function statistics(va1) {
    var dom = document.getElementById("container");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;
    option = {
        title: {
            text: '用例折线图:'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['总用例', '成功用例', '失败用例', '超时用例', '跳过用例']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '4%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['2019-3-1', '2019-3-2', '2019-3-3', '2019-3-4', '2019-3-5', '2019-3-6', '2019-3-7']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: '总用例',
                type: 'line',
                data: [va1,130, 101, 134, 90, 230, 210]
            },
            {
                name: '成功用例',
                type: 'line',
                data: [300,241, 191, 234, 290, 330, 310]
            },
            {
                name: '失败用例',
                type: 'line',
                data: [150, 232, 201, 154, 190, 330, 410]
            },
            {
                name: '超时用例',
                type: 'line',
                data: [320, 332, 301, 334, 390, 330, 320]
            },
            {
                name: '跳过用例',
                type: 'line',
                data: [200,89,78,86,34,45,234]
            }
        ]
    };
if (option && typeof option === "object") {
    myChart.setOption(option, true);
}
}

function search(csrf_token) {
   $("#search").on("click",function () {
        var value = $('#myid option:selected').val();
        $.ajax({
            url: "/platform/query/",
            type: "post",
            data: {"value": value,csrfmiddlewaretoken:'{{ csrf_token }}'},
            success: function (arg) {
                statistics(arg);
            }
        })
    })
}

function myclose(name,style) {
    var btn = document.getElementsByClassName(name)[0];
    btn.style.display=style;
}

function tips(){
    var tip = document.getElementById('tips');
    tip.style.display = 'block';
}

