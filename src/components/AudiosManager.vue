<template>
  <div style="display: flex" class="q-mb-sm q-pr-md">
    <q-pagination
      v-model="currentPage"
      :max="1000"
      input
      @update:model-value="(value) => fetchData()"
    />
    <q-space></q-space>
    <q-btn label="Add" color="teal" @click="addDialog = true"></q-btn>
    <q-dialog v-model="addDialog" @before-show="audioAdd.file = null">
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <q-input label="Enter name" type="text" dense v-model="audioAdd.name" />
        </q-card-section>
        <q-card-section>
          <q-file
            style="max-width: 300px"
            v-model="audioAdd.file"
            filled
            label="Select audio file"
            accept=".wav, .mp3"
          />
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn label="Add Audio" color="teal" v-close-popup @click="addAudio" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
  <div>
    <div style="border: solid rgb(192, 192, 192); border-width: 0px 0px 1px 0px">
      <div class="flex">
        <div
          style="
            width: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid rgb(192, 192, 192);
            border-width: 1px 0px 0px 1px;
          "
        >
          STT
        </div>
        <div
          style="
            width: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid rgb(192, 192, 192);
            border-width: 1px 0px 0px 1px;
          "
        >
          Name
        </div>
        <div
          style="
            flex-grow: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid rgb(192, 192, 192);
            border-width: 1px 0px 0px 1px;
          "
        >
          Audio
        </div>
        <div
          style="
            width: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid rgb(192, 192, 192);
            border-width: 1px 0px 0px 1px;
          "
        >
          Created Date
        </div>
        <div
          style="
            width: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid rgb(192, 192, 192);
            border-width: 1px 0px 0px 1px;
          "
        >
          Last Update
        </div>
        <div
          style="
            width: 160px;
            border: solid rgb(192, 192, 192);
            border-width: 1px 1px 0px 1px;
          "
        ></div>
      </div>
      <div v-for="(audio, index) in audios" :key="audio.id">
        <div class="flex">
          <div
            style="
              width: 50px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
          >
            {{ index + (this.currentPage - 1) * this.itemPerPage }}
          </div>
          <div
            style="
              width: 100px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
          >
            {{ audio.name }}
          </div>
          <div
            style="
              width: 150px;
              flex-grow: 1;
              display: flex;
              align-items: center;
              word-break: break-all;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
            class="q-pa-sm"
          >
            <audio controls>
              <source :src="`${ip}/audiourl/${audio.id}`" type="audio/wav" />
            </audio>
          </div>
          <div
            style="
              width: 150px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
            class="q-pa-sm"
          >
            {{ audio.date.split(".")[0] }}
          </div>
          <div
            style="
              width: 150px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
            class="q-pa-sm"
          >
            {{ audio.lastupdate.split(".")[0] }}
          </div>

          <div
            style="
              width: 160px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 1px 0px 1px;
            "
            class="q-pa-sm"
          >
            <q-btn
              style="width: fit-content"
              label="Edit"
              color="blue"
              @click="
                audioEdit = JSON.parse(JSON.stringify(audio));
                parseFileAudioEdit();
                editDialog = true;
              "
            >
            </q-btn>
            <q-btn
              class="q-ml-sm"
              style="width: fit-content"
              label="Delete"
              color="red"
              @click="deleteAudio(audio.id)"
            ></q-btn>
          </div>
        </div>
      </div>
    </div>
    <q-dialog v-model="editDialog" @before-show="audioEdit.file = null">
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <q-input type="text" dense v-model="audioEdit.name" />
        </q-card-section>
        <q-card-section>
          <q-file
            style="max-width: 300px"
            v-model="audioEdit.file"
            filled
            label="Select audio file"
            accept=".wav, .mp3"
          />
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn label="Accept" color="teal" v-close-popup @click="editAudio()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import axios from "axios";
import { onMounted } from "vue";

export default defineComponent({
  name: "AudiosManager",

  components: {},
  methods: {
    async addAudio() {
      let data = new FormData();
      data.append("name", this.audioAdd.name);
      data.append("audio", this.audioAdd.file);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/addaudio`,
        headers: {
          ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
        },
        data: data,
      };

      axios
        .request(config)
        .then((response) => {
          console.log(JSON.stringify(response.data));
          this.fetchData();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deleteAudio(id) {
      let data = new FormData();
      data.append("id", id);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/deleteaudio`,
        headers: {
          ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
        },
        data: data,
      };

      axios
        .request(config)
        .then((response) => {
          console.log(JSON.stringify(response.data));
          this.fetchData();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    editAudio() {
      let data = new FormData();
      data.append("id", this.audioEdit.id);
      data.append("name", this.audioEdit.name);
      data.append("audio", this.audioEdit.file);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/editaudio`,
        headers: {
          ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
        },
        data: data,
      };

      axios
        .request(config)
        .then((response) => {
          console.log(JSON.stringify(response.data));
          this.fetchData();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async parseFileAudioEdit() {
      var url = `${this.ip}/audiourl/${this.audioEdit.id}`;
      var response = await fetch(url);
      var blob = await response.blob();
      const fileName = this.audioEdit.path;
      const file = new File([blob], fileName, { type: blob.type });
      this.audioEdit.file = file;
    },
    fetchData() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/audios?start_idx=${
          (this.currentPage - 1) * this.itemPerPage
        }&count=${this.itemPerPage}`,
        headers: {},
      };

      axios
        .request(config)
        .then((response) => {
          this.audios = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  beforeMount() {
    this.fetchData();
  },
  data() {
    return {
      addDialog: false,
      editDialog: false,
      audioAdd: {
        name: "",
        file: null,
      },
      audioEdit: {
        name: "",
        file: null,
      },
      audios: [],
      currentPage: 1,
      itemPerPage: 5,
      ip: this.$ip,
      tab: "audio",
    };
  },
});
</script>
<style lang="sass"></style>
