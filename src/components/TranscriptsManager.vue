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
        contentAdd = '';
        nameAdd = '';
      "
    >
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <q-input type="text" label="Enter name" dense v-model="nameAdd" />
        </q-card-section>
        <q-card-section class="q-pt-none">
          <q-input type="textarea" label="Enter content" dense v-model="contentAdd" />
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
  <div>
    <q-list bordered class="rounded-borders">
      <q-item class="q-pa-none q-pr-sm">
        <q-item-section
          side
          style="width: 50px; align-items: center"
          class="text-black q-pa-none"
        >
          STT
        </q-item-section>
        <q-separator vertical />
        <q-item-section
          side
          style="width: 100px; align-items: center"
          class="text-black q-pa-none"
        >
          Name
        </q-item-section>
        <q-separator vertical />
        <q-item-section style="width: 100%; align-items: center" class="q-pa-none">
          Content
        </q-item-section>
        <q-separator vertical />
        <q-item-section
          side
          style="width: 150px; align-items: center"
          class="text-black q-pa-none"
        >
          Created Date
        </q-item-section>
        <q-separator vertical />
        <q-item-section
          side
          style="width: 150px; align-items: center"
          class="text-black q-pa-none"
        >
          Last Update
        </q-item-section>
        <q-separator vertical />
        <q-item-section side>
          <q-btn
            class="q-ml-sm"
            style="visibility: hidden; width: fit-content"
            label="Edit"
          >
          </q-btn>
        </q-item-section>
        <q-item-section side>
          <q-btn
            class="q-ml-sm"
            style="visibility: hidden; width: fit-content"
            label="Delete"
          ></q-btn>
        </q-item-section>
      </q-item>
      <q-separator />
      <div v-for="(transcript, index) in transcripts" :key="transcript.id">
        <q-item class="q-pa-none q-pr-sm">
          <q-item-section
            side
            style="width: 50px; align-items: center"
            class="text-black q-pa-none"
          >
            {{ index }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section
            side
            style="width: 100px; align-items: center"
            class="text-black q-pa-none"
          >
            {{ transcript.name }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section style="width: 100%" class="q-pa-none">
            <div class="q-px-sm">{{ transcript.content }}</div>
          </q-item-section>
          <q-separator vertical />
          <q-item-section
            side
            style="width: 150px; align-items: center"
            class="text-black q-pa-none"
          >
            {{ transcript.date }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section
            side
            style="width: 150px; align-items: center"
            class="text-black q-pa-none"
          >
            {{ transcript.update }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section side>
            <q-btn
              style="width: fit-content"
              label="Edit"
              color="blue"
              class="q-ml-sm"
              @click="
                transcriptEdit = transcript;
                contentEdit = transcript.content;
                nameEdit = transcript.name;
                editDialog = true;
              "
            >
            </q-btn>
          </q-item-section>
          <q-item-section side>
            <q-btn
              style="width: fit-content"
              label="Delete"
              color="red"
              class="q-ml-sm"
              @click="deleteTranscript(transcript.id)"
            ></q-btn>
          </q-item-section>
        </q-item>

        <q-separator spaced />
      </div>
    </q-list>
    <q-dialog v-model="editDialog">
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <q-input type="text" label="name" dense v-model="nameEdit" autofocus />
        </q-card-section>
        <q-card-section class="q-pt-none">
          <q-input
            type="textarea"
            label="content"
            dense
            v-model="contentEdit"
            autofocus
          />
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn
            label="Accept"
            color="teal"
            v-close-popup
            @click="
              editTranscript(
                transcriptEdit.id,
                transcriptEdit.content,
                transcriptEdit.name
              )
            "
          />
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
      data.append("content", this.contentAdd);
      data.append("name", this.nameAdd);
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

    editTranscript(id, content, name) {
      if (this.contentEdit != content || this.nameEdit != name) {
        let data = new FormData();
        data.append("id", id);
        data.append("content", this.contentEdit);
        data.append("name", this.nameEdit);
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
      }
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
      file: null,
      addDialog: false,
      editDialog: false,
      nameAdd: "",
      contentAdd: "",
      nameEdit: "",
      contentEdit: "",
      transcriptEdit: "",
      transcripts: [],
      currentPage: 1,
      itemPerPage: 5,
      ip: "http://localhost:80",
      tab: "transcript",
    };
  },
});
</script>
<style lang="sass">
.q-item__section--side
    padding-right: 0px
    padding-left: 0px

.q-item__section--main ~ .q-item__section--side
    padding-right: 0px
    padding-left: 0px
</style>
