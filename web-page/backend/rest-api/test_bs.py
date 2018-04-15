import bs4

html = """<q>Trả góp 1 tháng bn tiền và trong tg bao lâu ạ</q>
<a>Chào chị, Hiện bên em hỗ trợ trả góp cho sản phẩm này gói lãi suất 0% rất tiết kiệm của công ty tài chính HomeCredit với mức trả trước 17.395.000₫(50%) và góp trong 8 tháng (2.271.500₫/tháng) chị nha, giấy tờ cần có là CMND  bằng lái xe (hoặc hộ khẩu). Nếu chị quan tâm đến gói trả góp này, chị có thể để lại tên và số điện thoại để bên em liên hệ và hỗ trợ chị làm hồ sơ trả góp online chị nhé. Mong phản hồi từ chị.<a>
<q>Để chưc năng dộ sáng tự động trên iphone gây hao pin k ạ</q>
<a>Chào bạn, Theo mình thấy thì tính năng này tùy vào môi trường và nhu cầu bạn sử dụng, nếu bạn tắt tính năng này và để độ sáng thấp thì sẽ giúp tiết kiệm pin hơn bạn nhé  Thân chào bạn!<a>
<a>@Xuân Phúc:  thankss a ạ<a>
<q>Cho e hỏi sáng sớm ra mua dt trả gop dc k ạ</q>"""

soup = bs4.BeautifulSoup(html, "lxml")

for ultag in soup.findAll('q'):
    print(ultag.text)