//const axios = require('axios');

let notesVue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#notesApp',
    data: {
        homePage: "'s notes",
        allNote: ['teszt1', 'teszt2'],
        importantArray: []
    },
    methods: {
        getNotes: async function() {
            try {
                const response = await axios.get('note_list');
                this.allNote = response.data
                console.log(this.allNote)
                for(i=0; i<response.data.length; i++) {
                    this.importantArray.push(response.data[i].important)
                } 
            } catch (error) {
                console.error(error);
            }
        },
        delThisNote: async function(elem) {
            let index = this.allNote.findIndex(obj => obj.id == elem);
            this.allNote.splice(index, 1);
            this.importantArray.splice(index, 1);
            delJSON = JSON.stringify({'del_id': elem})
            try {
                await axios.post('delete_note/', delJSON)
            } catch (error) {
                console.error(error);
            }
        }
    },
    mounted() {
        this.getNotes();
    }
})