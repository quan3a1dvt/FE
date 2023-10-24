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
          <q-btn label="Add Audio" v-close-popup @click="addAudio" />
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
          Audio
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
      <div v-for="(audio, index) in audios" :key="audio.id">
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
            {{ audio.name }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section style="width: 100%" class="rm-pad">
            <audio controls>
              <source :src="`${ip}/audio/${audio.id}`" type="audio/wav" />
            </audio>
          </q-item-section>
          <q-separator vertical />
          <q-item-section
            side
            style="width: 150px; align-items: center"
            class="text-black rm-pad"
          >
            {{ audio.date }}
          </q-item-section>
          <q-separator vertical />
          <q-item-section
            side
            style="width: 150px; align-items: center"
            class="text-black rm-pad"
          >
            {{ audio.update }}
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
              @click="deleteAudio(audio.id)"
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
            @click="editAudio(audioEdit.id, audioEdit.name)"
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
  name: "AudiosManager",

  components: {},
  methods: {
    async addAudio() {
      let data = new FormData();
      data.append("name", this.nameAdd);
      data.append("audio", this.file);
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

    editAudio(id, name) {
      if (this.nameEdit != name) {
        let data = new FormData();
        data.append("id", id);

        data.append("name", this.nameEdit);
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
      }
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
      file: null,
      addDialog: false,
      editDialog: false,
      nameAdd: "",
      nameEdit: "",
      audioEdit: null,
      audios: [],
      currentPage: 1,
      itemPerPage: 5,
      ip: "http://localhost:80",
      tab: "audio",
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
