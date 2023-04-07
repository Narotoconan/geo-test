from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from util.driver import base, EC, sleep
import re


class PagePublish:
    def __init__(self):
        self.page = "/geoserver/web/wicket/bookmarkable/org.geoserver.web.data.layer.NewLayerPage"

        self.store_selection = By.XPATH, '//select[@name="storesDropDown"]'

        self.layer_search = By.ID, "filter"
        self.page_msg = By.XPATH, "//span[contains(text(), '的结果')]"
        self.next_page = By.XPATH, "//div[@class='leftwise']//a[@class='next']"
        self.layer_list = By.CSS_SELECTOR, '.clearBoth tbody tr'

        self.bounds_box = By.PARTIAL_LINK_TEXT, "从数据中计算"
        self.bounds_lat_lng = By.PARTIAL_LINK_TEXT, "Compute from native bounds"

        self.publish_btn = By.XPATH, '//*[@class="tabpanel"]//span[text()="发布"]'
        self.style_selection = By.ID, 'defaultStyle'

        self.save_btn = By.LINK_TEXT, '保存'
        ...

    def open_publish(self):
        base.base_page(self.page)

    def select_data_store(self, text: str):
        base.base_select(loc=self.store_selection, text=text)

    def get_page(self):
        msg = base.base_context(self.page_msg)
        start, end, total, result = re.findall(r'从(.*?)到(.*?)的结果\(在(.*?)个中有(.*?)个匹配项\)', msg)[0]
        return end.strip(), result.strip()

    def page_turning(self):
        # base.base_input(self.layer_search, Keys.ENTER, is_clear=False)
        end, total = self.get_page()
        if end != total:
            base.base_click(self.next_page)

    def select_layer(self, layer_name, first=True):
        if first:
            base.base_input(self.layer_search, layer_name)
            base.base_input(self.layer_search, Keys.ENTER, is_clear=False)
            sleep(1)
        layer = base.base_ec(
            EC.visibility_of_element_located((By.XPATH, f"//tbody//span[text()='{layer_name}']")),
            time_out=3
        )
        if not layer:
            end, result = self.get_page()
            if end == result:
                assert False, f"Layer: {layer_name}, 未找到"
            self.page_turning()
            self.select_layer(layer_name, False)
        else:
            l_status = base.base_get_element(
                (By.XPATH, f"//tbody//span[text()='{layer_name}']/parent::td/following-sibling::td[1]//a")
            )
            if l_status.text == '发布':
                l_status.click()
                sleep(1)  # 若后面无操作则需等待1秒
                return
            else:
                assert False, f"Layer: {layer_name}, 已发布"
    # def select_layer(self, layer_name: str):
    #     # 搜索layer名称
    #     base.base_input(self.layer_search, layer_name)
    #     base.base_input(self.layer_search, Keys.ENTER, is_clear=False)
    #
    #     sleep(1)
    #
    #     # 获取layer列表，找到layer点击发布
    #     layers = base.base_get_elements(self.layer_list)
    #     find_layer = False
    #
    #     assert layers is not None, f"Layer: {layer_name}, 未找到"
    #     for layer in layers:
    #         l_name = layer.find_element(By.CSS_SELECTOR, "td:nth-child(2) span")
    #         l_status = layer.find_element(By.CSS_SELECTOR, "td a")
    #         if layer_name == l_name.text:
    #             find_layer = True
    #             if l_status.text == '发布':
    #                 l_status.click()
    #             else:
    #                 assert False, f"Layer: {layer_name}, 已发布"
    #     else:
    #         assert find_layer, f"Layer: {layer_name}, 未找到"

    def bounds(self):
        sleep(1)
        scroll_y = base.base_get_element(self.bounds_box).location.get("y")
        base.base_script(f"window.scrollBy(0,{scroll_y})")

        base.base_click(self.bounds_box)
        base.base_click(self.bounds_lat_lng)

        sleep(1)
        base.base_script(f"window.scrollTo(0,0)")
        ...

    def style(self, style_name):
        # 点击发布页面
        base.base_click(self.publish_btn)
        # 滚动到样式选择框
        scroll_y = base.base_get_element(self.style_selection).location.get("y")
        base.base_script(f"window.scrollBy(0,{scroll_y})")

        # 选择样式名称
        base.base_select(self.style_selection, text=style_name)
        sleep(1)

    def sava_layer(self):
        base.base_click(self.save_btn)
