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
          <q-input type="text" dense v-model="nameAdd" />
        </q-card-section>
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
            <q-btn label="Find" color="teal" @click="getAudioByName(audioNameAdd)">
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
          <q-btn label="Add Sample" color="teal" v-close-popup @click="addSample()" />
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
          Content
        </div>
        <div
          style="
            width: 300px;
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
            width: 160px;
            border: solid rgb(192, 192, 192);
            border-width: 1px 1px 0px 1px;
          "
        ></div>
      </div>
      <q-separator />
      <div v-for="(sample, index) in samples" :key="sample.id">
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
            {{ sample.name }}
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
            {{ transcripts[sample.transcriptId].content }}
          </div>
          <div
            style="
              width: 300px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
          >
            <audio controls>
              <source :src="`${ip}/audiourl/${sample.audioId}`" type="audio/wav" />
            </audio>
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
                sampleEdit = JSON.parse(JSON.stringify(sample));
                editDialog = true;
              "
            >
            </q-btn>
            <q-btn
              class="q-ml-sm"
              style="width: fit-content"
              label="Delete"
              color="red"
              @click="deleteSample(sample.id)"
            ></q-btn>
          </div>
        </div>
      </div>
    </div>
    <q-dialog v-model="editDialog" @before-show="editSetup()">
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <q-input type="text" dense v-model="nameEdit" />
        </q-card-section>
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
          <q-btn label="Accept" color="teal" v-close-popup @click="editSample()" />
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
      data.append("name", this.nameAdd);
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
    editSetup() {
      this.nameEdit = this.sampleEdit.name;
      this.transcriptNameEdit = this.transcripts[this.sampleEdit.transcriptId].name;
      this.audioNameEdit = this.audios[this.sampleEdit.audioId].name;
      this.searchTranscript = JSON.parse(
        JSON.stringify(this.transcripts[this.sampleEdit.transcriptId])
      );
      this.searchAudio = JSON.parse(JSON.stringify(this.audios[this.sampleEdit.audioId]));
    },
    editSample() {
      let data = new FormData();
      data.append("id", this.sampleEdit.id);
      data.append("name", this.nameEdit);
      data.append("audioId", this.searchAudio.id);
      data.append("transcriptId", this.searchTranscript.id);
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

      var res = await axios.request(config);
      return res["data"];
    },
    async fetchAudio(id) {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/audio?id=${id}`,
        headers: {},
      };
      var res = await axios.request(config);
      return res["data"];
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
      addDialog: false,
      editDialog: false,
      nameAdd: "",
      nameEdit: "",
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
