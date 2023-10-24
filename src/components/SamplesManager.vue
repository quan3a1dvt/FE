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
          <q-input type="textarea" dense v-model="contentAdd" />
        </q-card-section>
        <q-card-section>
          <q-file
            style="max-width: 300px"
            v-model="file"
            filled
            label="Select audio file"
            accept=".wav, .mp3"
          />
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn label="Add Sample" v-close-popup @click="addSample" />
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
        <q-item-section style="width: 100%; align-items: center" class="rm-pad">
          Content
        </q-item-section>
        <q-separator vertical />
        <q-item-section side style="width: 350px; align-items: center" class="rm-pad">
          Audio
        </q-item-section>
        <q-separator vertical />
        <q-item-section side>
          <q-btn style="visibility: hidden; width: fit-content" label="Edit"> </q-btn>
        </q-item-section>
        <q-item-section side>
          <q-btn style="visibility: hidden; width: fit-content" label="Delete"></q-btn>
        </q-item-section>
      </q-item>
      <q-separator />
      <div v-for="(sample, index) in samples" :key="sample.id">
        <q-item>
          <q-item-section
            side
            style="width: 50px; align-items: center"
            class="text-black rm-pad"
          >
            {{ index }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section style="width: 100%" class="text-black rm-pad">
            {{ sample.content }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section side style="width: 350px" class="rm-pad">
            <audio controls>
              <source :src="`${ip}/audio/${sample.audioId}`" type="audio/wav" />
            </audio>
          </q-item-section>
          <q-item-section side>
            <q-btn
              style="width: fit-content"
              label="Edit"
              color="blue"
              @click="
                audioEdit = audio;
                contentEdit = audio.content;
                nameEdit = audio.name;
                editDialog = true;
              "
            >
            </q-btn>
          </q-item-section>
          <q-item-section side class="">
            <q-btn
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
    <q-dialog v-model="editDialog" persistent>
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <q-input type="text" dense v-model="nameEdit" autofocus />
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn
            label="Accept"
            color="green"
            v-close-popup
            @click="editSample(audioEdit.id, audioEdit.name)"
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
    async addSample() {
      let data = new FormData();
      data.append("content", this.contentAdd);
      data.append("audio", this.file);
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
          console.log(JSON.stringify(response.data));
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
          console.log(JSON.stringify(response.data));
          this.fetchData();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    editSample(id, name) {
      if (this.nameEdit != name) {
        let data = new FormData();
        data.append("id", id);

        data.append("name", this.nameEdit);
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
      }
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
        .then((response) => {
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
      addDialog: false,
      editDialog: false,
      nameAdd: "",
      nameEdit: "",
      contentAdd: "",
      samples: [],
      currentPage: 1,
      itemPerPage: 5,
      ip: "http://localhost:80",
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
