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
    <q-dialog v-model="addDialog" @before-show="file = null">
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <div class="flex q-pt-md">
            <q-input
              style="width: 240px"
              label="Enter transcript name"
              type="text"
              dense
              v-model="transcriptNameAdd"
            />
            <q-space />
            <q-btn
              label="Find"
              color="teal"
              @click="getTranscriptByName(transcriptNameAdd)"
            >
            </q-btn>
          </div>
          <div v-if="searchTranscript != null" class="q-pt-sm">
            {{ searchTranscript.content }}
          </div>
        </q-card-section>
        <q-card-section class="q-pt-none">
          <div class="flex q-pt-md">
            <q-input
              style="width: 240px"
              label="Enter audio name"
              type="text"
              dense
              v-model="audioNameAdd"
            />
            <q-space />
            <q-btn label="Find" color="teal" @click="getAudioByName(audioNameEdit)">
            </q-btn>
          </div>
          <div v-if="searchAudio != null" class="q-pt-sm">
            <audio controls>
              <source :src="`${ip}/audiourl/${searchAudio.id}`" type="audio/wav" />
            </audio>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn label="Add Sample" color="teal" v-close-popup @click="addSample" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
  <div>
    <q-list bordered class="rounded-borders">
      <q-item class="q-pa-none q-pr-sm">
        <q-item-section side style="width: 50px; align-items: center" class="text-black">
          STT
        </q-item-section>
        <q-separator vertical />
        <q-item-section style="width: 100%; align-items: center" class="text-black">
          Content
        </q-item-section>
        <q-separator vertical />
        <q-item-section side style="width: 320px; align-items: center" class="">
          Audio
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
      <div v-for="(sample, index) in samples" :key="sample.id">
        <q-item class="q-pa-none q-pr-sm">
          <q-item-section
            side
            style="width: 50px; align-items: center"
            class="text-black"
          >
            {{ index }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section style="width: 100%; align-items: center" class="text-black">
            {{ sample.content }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section side style="width: 320px" class="">
            <div class="q-pl-sm q-pt-sm">
              <audio controls>
                <source :src="`${ip}/audiourl/${sample.audioId}`" type="audio/wav" />
              </audio>
            </div>
          </q-item-section>
          <q-separator vertical />
          <q-item-section side>
            <q-btn
              class="q-ml-sm"
              style="width: fit-content"
              label="Edit"
              color="blue"
              @click="
                sampleEdit = sample;
                editDialog = true;
              "
            >
            </q-btn>
          </q-item-section>
          <q-item-section side class="">
            <q-btn
              class="q-ml-sm"
              style="width: fit-content"
              label="Delete"
              color="red"
              @click="deleteSample(sample.id)"
            ></q-btn>
          </q-item-section>
        </q-item>

        <q-separator spaced />
      </div>
    </q-list>
    <q-dialog
      v-model="editDialog"
      @before-show="
        searchTranscript = null;
        searchAudio = null;
        transcriptNameEdit = sampleEdit.transcriptName;
        audioNameEdit = sampleEdit.audioName;
      "
    >
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <div class="flex q-pt-md">
            <q-input
              style="width: 240px"
              label="Enter transcript name"
              type="text"
              dense
              v-model="transcriptNameEdit"
            />
            <q-space />
            <q-btn
              label="Find"
              color="teal"
              @click="getTranscriptByName(transcriptNameEdit)"
            >
            </q-btn>
          </div>
          <div v-if="searchTranscript != null" class="q-pt-sm">
            {{ searchTranscript.content }}
          </div>
        </q-card-section>
        <q-card-section class="q-pt-none">
          <div class="flex q-pt-md">
            <q-input
              style="width: 240px"
              label="Enter audio name"
              type="text"
              dense
              v-model="audioNameEdit"
            />
            <q-space />
            <q-btn label="Find" color="teal" @click="getAudioByName(audioNameEdit)">
            </q-btn>
          </div>
          <div v-if="searchAudio != null" class="q-pt-sm">
            <audio controls>
              <source :src="`${ip}/audiourl/${searchAudio.id}`" type="audio/wav" />
            </audio>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn
            label="Accept"
            color="teal"
            v-close-popup
            @click="editSample(sampleEdit.id, searchAudio.id, searchTranscript.id)"
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
  name: "SamplesManager",
  components: {},
  methods: {
    getTranscriptByName(name) {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/transcript-by-name?name=${name}`,
        headers: {},
      };

      axios
        .request(config)
        .then((response) => {
          this.searchTranscript = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getAudioByName(name) {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/audio-by-name?name=${name}`,
        headers: {},
      };

      axios
        .request(config)
        .then((response) => {
          this.searchAudio = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async addSample() {
      let data = new FormData();
      data.append("audioId", this.searchAudio.id);
      data.append("transcriptId", this.searchTranscript.id);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/addsample`,
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
          this.fetchData();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deleteSample(id) {
      let data = new FormData();
      data.append("id", id);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/deletesample`,
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
          this.fetchData();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    editSample(id, audioId, transcriptId) {
      let data = new FormData();
      data.append("id", id);
      data.append("audioId", audioId);
      data.append("transcriptId", transcriptId);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/editsample`,
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
    async fetchTranscript(id) {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/transcript?id=${id}`,
        headers: {},
      };

      axios
        .request(config)
        .then((response) => {
          var transcript = response.data;
          return transcript;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async fetchAudio(id) {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/audio?id=${id}`,
        headers: {},
      };

      axios
        .request(config)
        .then((response) => {
          var audio = response.data;
          return audio;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchData() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/samples?start_idx=${
          (this.currentPage - 1) * this.itemPerPage
        }&count=${this.itemPerPage}`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          var samples = response.data;
          for (var sample of samples) {
            var transcript = await this.fetchTranscript(sample.transcriptId);
            var audio = await this.fetchAudio(sample.audioId);
            this.transcripts[transcript.id] = transcript;
            this.audios[audio.id] = audio;
          }
          this.samples = response.data;
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
      fileEdit: null,
      addDialog: false,
      editDialog: false,
      sampleEdit: "",

      transcriptNameAdd: "",
      audioNameAdd: "",
      transcriptNameEdit: "",
      audioNameEdit: "",
      searchTranscript: null,
      searchAudio: null,
      samples: [],
      transcripts: {},
      audios: {},
      currentPage: 1,
      itemPerPage: 5,
      ip: this.$ip,
    };
  },
});
</script>
<style lang="sass"></style>
