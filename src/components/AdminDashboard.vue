<template>
    <div>
        <h1>Welcome to admin page</h1>

        <div>
            <h3>Create Category</h3>
            <form @submit.prevent="createCategory">
                <label for="newCategory">Category Name:</label>
                <input type="text" id="newCategory" v-model="newCategoryName" required>
                <button type="submit">Create Category</button>
            </form>
        </div>

        <div>
            <h3>Existing Categories</h3>
            <ul>
                <li v-for="category in categories" :key="category.id">
                    {{ category.name }}
                    <button @click="editCategory(category.id, category.name)">Edit</button>
                    <button @click="confirmDelete(category.id)">Delete</button>

                </li>
            </ul>
        </div>

        <div v-if="editingCategory">
            <div class="modal-overlay" @click="cancelEdit"></div>
            <div class="modal-content">
                <h3>Edit Category</h3>
                <label for="editedCategory">New Category Name</label>
                <input type="text" id="editedCategory" v-model="editedCategoryName" required>
                <button @click="saveEdit">Save</button>
                <button @click="cancelEdit">Cancel</button>
            </div>
        </div>

        <div v-if="confirmingDelete">
            <div class="modal-overlay" @click="cancelDelete"></div>
            <div class="modal-content">
                <h3>Confirm Delete</h3>
                <!-- <p>jake apne Ex ka number delete kar mujhe nhi &#128540; </p> -->
                 <p>Are you sure you want to delete this category?</p>
                <br>
                <button @click="deleteCategory">Yes, Delete</button>
                <button @click="cancelDelete">Cancel</button>

            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            categories: [],
            newCategoryName: '',
            editingCategory: null,
            editedCategoryName: '',
            confirmingDelete: null
        }
    },
    mounted(){
        this.fetchCategories();
    },
    methods: {
        async fetchCategories() {
            try {
                const response = await axios.get('/categories');
                this.categories = response.data;
            } catch (error) {
                console.error(error);
            }
        },
        async createCategory() {
            try {
                const response = await axios.post('/categories', { name: this.newCategoryName });
                console.log(response.data);
                this.fetchCategories();
                this.newCategoryName = ''; // clear the input field after submission
            } catch (error) {
                console.error(error.response.data);
            }
        },
        editCategory(categoryId, categoryName) {
            this.editingCategory = categoryId;
            this.editedCategoryName = categoryName;
        },
        saveEdit() {
            axios.put(`/categories/${this.editingCategory}`, { name: this.editedCategoryName })
                .then(response => {
                    console.log(response.data);
                    this.fetchCategories();
                    this.cancelEdit();
                })
                .catch(error => {
                    console.error(error.response.data);
                });
        },
        cancelEdit() {
            this.editingCategory = null;
            this.editedCategoryName = '';
        },
        confirmDelete(categoryId) {
            this.confirmingDelete = categoryId;
        },
        deleteCategory() {
            axios.delete(`/categories/${this.confirmingDelete}`)
                .then(response => {
                    console.log(response.data);
                    this.fetchCategories();
                    this.confirmingDelete = null;
                })
                .catch(error => {
                    console.error(error.response.data);
                });
        },
        cancelDelete() {
            this.confirmingDelete = null;
        }
    }
}
</script>

<style>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1;
}

.modal-content {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 20px;
    z-index: 2;
    border-radius: 5px;
}
</style>
