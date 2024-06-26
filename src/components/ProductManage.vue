<template>
    <div class="container">
        <div class="add_product">
            <h1>Add Product</h1>
            <form @submit.prevent="addProduct">
                <table>
                    <thead>
                        <tr>
                            <th>Product Name</th>
                            <th>Expiry Date</th>
                            <th>Manufacture Date</th>
                            <th>Category</th>
                            <th>Price</th>
                            <th>Unit</th>
                            <th>Quantity</th>
                            <th>Action</th>

                            
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><input type="text" v-model="productName" placeholder="Product Name" required></td>
                            <td><input type="date" v-model="expiryDate" required></td>
                            <td><input type="date" v-model="manufactureDate" required></td>
                            <td>
                                <select v-model="selectedCategory" required>
                                    <option v-for="category in categories" :key="category.id" :value="category.name">
                                        {{ category.name }}
                                    </option>
                                </select>
                            </td>
                            <td><input type="number" v-model="price" step="0.01" placeholder="Price" required></td>
                            <td>
                                <select v-model="unit" required>
                                    <option value="piece">Piece</option>
                                    <option value="Kg">Kilogram</option>
                                    <option value="Litre">Litre</option>
                                </select>
                            </td>
                            <td><input type="number" v-model="quantity" placeholder="Quantity" required></td>
                            <td><button type="submit">Add Product</button></td>
                        </tr>
                    </tbody>
                </table>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            productName: '',
            expiryDate: '',
            manufactureDate: '',
            selectedCategory: '',
            price: 0,
            unit: 'piece',
            quantity: 0,
            categories: []
        };
    },
    mounted() {
        this.fetchCategories();
    },
    methods: {
        async fetchCategories() {
            try {
                const response = await axios.get('/categories', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`
                    }
                });
                this.categories = response.data;
            } catch (error) {
                console.error(error);
            }
        },
        async addProduct() {
            try {
                const productData = {
                    name: this.productName,
                    expiry_date: this.expiryDate,
                    manufacture_date: this.manufactureDate,
                    category: this.selectedCategory,
                    price: this.price,
                    unit: this.unit,
                    quantity: this.quantity
                };
                const response = await axios.post('/products', productData, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`
                    }
                });
                console.log(response.data);
                // Clear the form
                this.productName = '';
                this.expiryDate = '';
                this.manufactureDate = '';
                this.selectedCategory = '';
                this.price = 0;
                this.unit = 'piece';
                this.quantity = 0;
            } catch (error) {
                console.error(error.response.data);
            }
        }
    }
};
</script>


<style scoped>
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.add_product h1 {
    text-align: center;
    margin-bottom: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    padding: 10px;
    border: 1px solid #ccc;
    text-align: left;
}

input, select, button {
    width: 100%;
    padding: 8px;
    margin: 5px 0;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
</style>
