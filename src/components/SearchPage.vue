<template>
    <div class="search-container">
        <h1>Product Searcher</h1>

        <form @submit.prevent="searchProducts">
            <input type="text" name="search_query" v-model="searchQuery" placeholder="Search...">
            <button type="submit">Search</button>
        </form>

        <h1><b>Search Results</b></h1>

        <div v-if="products.length > 0">
            <table>
                <thead>
                    <tr>
                        <th>Product Name</th>
                        <th>Category</th>
                        <th>Price</th>
                        <th>Manufacture Date</th>
                        <th>Available</th>
                        <th>Quantity</th>
                        <th>Add to Cart</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in products" :key="product.id">
                        <td>{{ product.name }}</td>
                        <td>{{ product.category }}</td>
                        <td>{{ product.price }}</td>
                        <td>{{ product.manufactureDate }}</td>
                        <td>{{ product.available }}</td>
                        <td>{{ product.quantity }}</td>
                        <td><button @click="addToCart(product)">Add to Cart</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else>No Results found</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            searchQuery: '',
            products: [],
            user_id: localStorage.getItem('user_id') // Get the user ID from localStorage
        }
    },
    methods: {
        searchProducts() {
            axios.post(`/api/customer/${this.user_id}/search`, { searchQuery: this.searchQuery })
                .then(response => {
                    this.products = response.data;
                })
                .catch(error => {
                    console.error(error);
                });
        },
        addToCart(product) {
            // Add product to cart logic
            console.log(`Product ${product.name} added to cart`);
        }
    }
}
</script>
