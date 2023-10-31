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
    <q-dialog
      v-model="addDialog"
      @before-show="
        transcriptAdd.content = '';
        transcriptAdd.name = '';
      "
    >
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <q-input type="text" label="Enter name" dense v-model="transcriptAdd.name" />
        </q-card-section>
        <q-card-section class="q-pt-none">
          <q-input
            type="textarea"
            label="Enter content"
            dense
            v-model="transcriptAdd.content"
          />
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn
            label="Add Transcript"
            color="teal"
            v-close-popup
            @click="addTranscript"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
  <div style="border: solid rgb(192, 192, 192); border-width: 0px 0px 1px 0px">
    <div>
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
          Content
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
    </div>
    <div v-for="(transcript, index) in transcripts" :key="transcript.id">
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
          {{ transcript.name }}
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
          {{ transcript.content }}
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
          {{ transcript.date.split(".")[0] }}
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
          {{ transcript.lastupdate.split(".")[0] }}
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
              transcriptEdit = JSON.parse(JSON.stringify(transcript));
              editDialog = true;
            "
          ></q-btn>
          <q-btn
            style="width: fit-content"
            label="Delete"
            color="red"
            class="q-ml-sm"
            @click="deleteTranscript(transcript.id)"
          ></q-btn>
        </div>
      </div>
    </div>

    <q-dialog v-model="editDialog">
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <q-input type="text" label="name" dense v-model="transcriptEdit.name" />
        </q-card-section>
        <q-card-section class="q-pt-none">
          <q-input
            type="textarea"
            label="content"
            dense
            v-model="transcriptEdit.content"
          />
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn label="Accept" color="teal" v-close-popup @click="editTranscript()" />
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
  name: "TranscriptsManager",

  components: {},
  methods: {
    async addTranscript() {
      let data = new FormData();
      data.append("content", this.transcriptAdd.content);
      data.append("name", this.transcriptAdd.name);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/addtranscript`,
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
    deleteTranscript(id) {
      let data = new FormData();
      data.append("id", id);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/deletetranscript`,
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

    editTranscript() {
      let data = new FormData();
      data.append("id", this.transcriptEdit.id);
      data.append("content", this.transcriptEdit.content);
      data.append("name", this.transcriptEdit.name);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/edittranscript`,
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
    fetchData() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/transcripts?start_idx=${
          (this.currentPage - 1) * this.itemPerPage
        }&count=${this.itemPerPage}`,
        headers: {},
      };

      axios
        .request(config)
        .then((response) => {
          this.transcripts = response.data;
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
      transcriptAdd: {
        name: "",
        content: "",
      },
      transcriptEdit: {
        name: "",
        content: "",
      },
      transcripts: [],
      currentPage: 1,
      itemPerPage: 5,
      ip: this.$ip,
      tab: "transcript",
    };
  },
});
</script>
<style lang="sass"></style>
