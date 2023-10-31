<template>
  <div>
    <q-select
      filled
      stack-label
      dense
      v-model="ttmId"
      :options="ttmOptions"
      label="Text to Mels"
      emit-value
      map-options
    />
    <q-select
      filled
      stack-label
      dense
      v-model="vocoderId"
      :options="vocoderOptions"
      label="Vocoder"
      emit-value
      map-options
    />
    <q-btn label="Select" color="teal" @click="SelectModel()"></q-btn>
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
    SelectModel() {
      let data = new FormData();
      data.append("ttmId", this.ttmId);
      data.append("vocoderId", this.vocoderId);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/model`,
        headers: {
          ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
        },
        data: data,
      };

      axios
        .request(config)
        .then((response) => {})
        .catch((error) => {
          console.log(error);
        });
    },
    fetchTtm() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/ttms`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          this.ttms = response.data;
          this.ttmOptions = [];
          for (var ttm of this.ttms) {
            this.ttmOptions.push({
              label: ttm.name,
              value: ttm.id,
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchVocoder() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/vocoders`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          this.vocoders = response.data;
          this.vocoderOptions = [];
          for (var vocoder of this.vocoders) {
            this.vocoderOptions.push({
              label: vocoder.name,
              value: vocoder.id,
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
      ttms: [],
      ttmOptions: [],
      vocoders: [],
      vocoderOptions: [],
      ip: this.$ip,
    };
  },
});
</script>
