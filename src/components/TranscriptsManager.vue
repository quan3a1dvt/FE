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
    <q-dialog v-model="addDialog" persistent>
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <q-input type="text" dense v-model="nameAdd" />
        </q-card-section>
        <q-card-section class="q-pt-none">
          <q-input type="textarea" dense v-model="contentAdd" />
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn label="Add Transcript" v-close-popup @click="addTranscript" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
  <div>
    <q-list bordered class="rounded-borders">
      <q-item>
        <q-item-section
          side
          style="width: 50px; align-items: center"
          class="text-black rm-pad"
        >
          STT
        </q-item-section>
        <q-separator vertical />
        <q-item-section
          side
          style="width: 100px; align-items: center"
          class="text-black rm-pad"
        >
          Name
        </q-item-section>
        <q-separator vertical />
        <q-item-section style="width: 100%; align-items: center" class="rm-pad">
          Content
        </q-item-section>
        <q-separator vertical />
        <q-item-section
          side
          style="width: 150px; align-items: center"
          class="text-black rm-pad"
        >
          Created Date
        </q-item-section>
        <q-separator vertical />
        <q-item-section
          side
          style="width: 150px; align-items: center"
          class="text-black rm-pad"
        >
          Last Update
        </q-item-section>
        <q-item-section side>
          <q-btn style="visibility: hidden; width: fit-content" label="Edit"> </q-btn>
        </q-item-section>
        <q-item-section side>
          <q-btn style="visibility: hidden; width: fit-content" label="Delete"></q-btn>
        </q-item-section>
      </q-item>
      <q-separator />
      <div v-for="(transcript, index) in transcripts" :key="transcript.id">
        <q-item>
          <q-item-section
            side
            style="width: 50px; align-items: center"
            class="text-black rm-pad"
          >
            {{ index }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section
            side
            style="width: 100px; align-items: center"
            class="text-black rm-pad"
          >
            {{ transcript.name }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section style="width: 100%" class="rm-pad">
            {{ transcript.content }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section
            side
            style="width: 150px; align-items: center"
            class="text-black rm-pad"
          >
            {{ transcript.date }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section
            side
            style="width: 150px; align-items: center"
            class="text-black rm-pad"
          >
            {{ transcript.update }}
          </q-item-section>
          <q-item-section side>
            <q-btn
              style="width: fit-content"
              label="Edit"
              color="blue"
              @click="editDialog = true"
            >
            </q-btn>
            <q-dialog
              v-model="editDialog"
              persistent
              @before-show="
                contentEdit = transcript.content;
                nameEdit = transcript.name;
              "
            >
              <q-card style="min-width: 350px">
                <q-card-section class="q-pt-none">
                  <q-input type="text" dense v-model="nameEdit" autofocus />
                </q-card-section>
                <q-card-section class="q-pt-none">
                  <q-input type="textarea" dense v-model="contentEdit" autofocus />
                </q-card-section>
                <q-card-actions align="right" class="text-primary">
                  <q-btn label="Cancel" v-close-popup />
                  <q-btn
                    label="Accept"
                    color="green"
                    v-close-popup
                    @click="
                      editTranscript(transcript.id, transcript.content, transcript.name)
                    "
                  />
                </q-card-actions>
              </q-card>
            </q-dialog>
          </q-item-section>
          <q-item-section side class="">
            <q-btn
              style="width: fit-content"
              label="Delete"
              color="red"
              @click="deleteTranscript(transcript.id)"
            ></q-btn>
          </q-item-section>
        </q-item>

        <q-separator spaced />
      </div>
    </q-list>
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
      transcripts: [],
      currentPage: 1,
      itemPerPage: 5,
      ip: "https://1229-14-231-130-155.ngrok-free.app",
      tab: "transcript",
    };
  },
});
</script>
<style lang="sass">
.rm-pad
    .q-item__section--side
        padding-right: 0px
        padding-left: 0px
</style>
