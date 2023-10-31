<template>
  <div>
    <q-select
      filled
      stack-label
      dense
      v-model="ttmId"
      :options="datasetOptions"
      label="Text to Mels"
      emit-value
      map-options
      @update:model-value="
        (value) => {
          fetchSamples();
          currentPage = 1;
        }
      "
    />
  </div>
</template>
<script>
import { defineComponent, ref } from "vue";
import axios from "axios";
import { onMounted } from "vue";

export default defineComponent({
  name: "ModelsManager",
  components: {},
  methods: {
    fetchData() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/datasets`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          this.datasets = response.data;
          this.datasetOptions = [];
          for (var dataset of this.datasets) {
            this.datasetOptions.push({
              label: dataset.name,
              value: dataset.id,
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  beforeMount() {
    // this.fetchData();
  },
  data() {
    return {
      ttmId: null,
      vocoderId: null,
      currentPage: 1,
      itemPerPage: 5,
      ip: this.$ip,
    };
  },
});
</script>
