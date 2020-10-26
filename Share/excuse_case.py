import requests


def excuse_case():

    url = "https://2008145027-site.pool202.yun300.cn/manager/gwforward/manager-webapi/content/infoCategory/editInfoCategory"
    h = {"Content-Type":"application/json;charset=UTF-8","Cookie":"GWSESSION=ODk0OWUzNmMtNDRlZC00ODI0LThkYmUtMTg1Njg0OGU3OWVl"}
    json = {"id":19,"parentId":"","parentName":"","name":"普通分类","imgUrl":"","type":"1","des":"<p>普通--分类</p>\n","mobileDes":"<p>普通--分类</p>\n","summary":"","keywords":"","targetType":"true","linkUrl":"","mobileTargetType":"true","mobileLinkUrl":"","showFlag":"true","mobileShowFlag":"true","newOpen":"true","showStyle":"","detailStyle":"","configValue":"","seoState":"true","seoTitle":[{"id":"categoryName","name":"资讯分类名称"},{"id":"oneCategoryName","name":"资讯分类一级分类名称"},{"id":"siteName","name":"网站名称"}],"seoTitleSign":"_","seoKeywords":[{"id":"categoryKeyword","name":"资讯分类关键词"},{"id":"siteName","name":"网站名称"}],"seoKeywordsSign":",","seoDescription":[{"id":"categoryName","name":"资讯分类名称"},{"id":"siteName","name":"网站名称"},{"id":"categoryDescription","name":"资讯分类描述"}],"seoDescriptionSign":"-","mobileNewOpen":"true","mobileShowStyle":"","mobileDetailStyle":"","authType":1,"authStr":"GW_:3:category:view:19","roleIds":"","authData":[{"authType":1,"authStr":"GW_:3:category:view:19","roleIds":""}]}
    r = requests.post(url,json=json,headers=h)
    return r.json()
