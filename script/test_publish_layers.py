from page.page_publish_layers import PagePublish
import pytest

publish = PagePublish()


class TestPublishLayers:

    @pytest.mark.parametrize("layer", ['1'])
    def test_publish(self, layer):
        publish.open_publish()

        publish.select_data_store("yancao_arc:yancao_arc")
        publish.select_layer(layer)

        # publish.bounds()
        # publish.style("yancao_arc:1_yancao_arc")

        # publish.sava_layer()
