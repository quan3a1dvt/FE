<template>
    <div style="display:flex" class="q-mb-sm q-pr-md">
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
                <q-input type="textarea" dense v-model="contentAdd" autofocus />
            </q-card-section>
            <q-card-section class="q-pt-none">
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
                <q-btn label="Add Sample" v-close-popup @click="AddSample" />
            </q-card-actions>
            </q-card>
        </q-dialog>
    </div>
    <div>
        <q-list bordered class="rounded-borders">
            <div v-for="(sample, index) in samples" :key="sample.id">
            <q-item>
                <q-item-section side style="width:fit-content" >
                {{index}}
                </q-item-section>
                <q-item-section >
                {{sample.content}}
                </q-item-section>
                <q-item-section  side>
                <audio controls>
                    <source :src="`${ip}/audio/${sample.audioId}`" type="audio/wav">
                </audio>
                </q-item-section>
                <q-item-section  side> 
                <q-btn style="width: fit-content" label="Edit" color="blue" @click="editDialog = true; contentEdit=sample.content">
                </q-btn>
                <q-dialog v-model="editDialog" persistent>
                    <q-card style="min-width: 350px">
                    <q-card-section class="q-pt-none">
                        <q-input type="textarea" dense v-model="contentEdit" autofocus />
                    </q-card-section>
                    <q-card-actions align="right" class="text-primary">
                        <q-btn label="Cancel" v-close-popup />
                        <q-btn label="Accept" color="green" v-close-popup @click="editTranscript(sample.transcriptId, sample.content)" />
                    </q-card-actions>
                    </q-card>
                </q-dialog>
                </q-item-section>
                <q-item-section  side>
                <q-btn style="width: fit-content" label="Delete" color="red" @click="deleteSample(sample.id)"></q-btn>
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
import { onMounted } from 'vue';

onMounted(() => {
    this.fetchData()
})

export default defineComponent({
name: "SamplesManager",
components: {},
methods: {
    async AddSample() {
        let data = new FormData();
        data.append('content', this.contentAdd);
        data.append('audio', this.file);

        let config = {
            method: 'post',
            maxBodyLength: Infinity,
            url: `${this.ip}/addsample`,
            headers: {
            ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
            },
            data : data
        };

        axios.request(config)
        .then((response) => {
            console.log(JSON.stringify(response.data));
        })
        .catch((error) => {
            console.log(error);
        });
    },
    deleteSample(id) {
        let data = new FormData();
        data.append('id', id);
        let config = {
            method: 'post',
            maxBodyLength: Infinity,
            url: `${this.ip}/deletesample`,
            headers: {
            ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
            },
            data : data
        };

        axios.request(config)
        .then((response) => {
            console.log(JSON.stringify(response.data));
        })
        .catch((error) => {
            console.log(error);
        });
    },

    editTranscript(id, content) {
    if (this.contentEdit != content) {
        let data = new FormData();
        data.append('id', id );
        data.append('content', this.contentEdit);
        let config = {
            method: 'post',
            maxBodyLength: Infinity,
            url: `${this.ip}/edittranscript`,
            headers: {
            ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
            },
            data : data
        };

        axios.request(config)
        .then((response) => {
            console.log(JSON.stringify(response.data));
        })
        .catch((error) => {
            console.log(error);
        });
    
    }
    },
    fetchData() {
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: `${this.ip}/samples?start_idx=${(this.currentPage - 1) * this.itemPerPage}&count=${this.itemPerPage}`,
            headers: {},
        };

        axios.request(config)
        .then((response) => {
            this.samples = response.data;
        })
        .catch((error) => {
            console.log(error);
        });

    }
},

data() {
    return {
        file: null,
        addDialog: false,
        editDialog: false,
        contentAdd: "",
        contentEdit: "",
        samples: [],
        currentPage: 1,
        itemPerPage: 5,
        ip: "http://localhost:80",
        tab: "sample"
    };
},
});
</script>
  