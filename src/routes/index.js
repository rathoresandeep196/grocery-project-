import {createRouter, createWebHistory} from 'vue-router'

import HelloWorld from '../components/DashboardComponent.vue'
import LoginPage from '../components/HelloWorld.vue'
import SignupPage from '../components/UserSignup.vue'
import AdminDasshboard from '../components/AdminDashboard.vue'
import ProductManage from '../components/ProductManage.vue'
import SearchPage from '../components/SearchPage.vue'


const routes = [
    {
        path: '/login',
        name: 'LoginPage', // same import one 
        component: LoginPage,
    }
    ,
    {
        path: '/admin',
        name: 'AdminDasshboard', // same import one  
        component: AdminDasshboard,
        meta: {
            isAdmin: true
        }
    }
    ,
    {
        path: '/',
        name: 'HelloWorld', // same import one 
        component: HelloWorld,
    },
    {
        path: '/search',
        name: 'search', // same import one 
        component: SearchPage,
    },
    {
        path: '/productmanage',
        name: 'ProductManage', // same import one 
        component:ProductManage,
    },
    {
        path: '/signup',
        name: 'SignupPage', // same import one 
        component: SignupPage,
    }
]

// export default createRouter({
//     history: createWebHistory(),
//     routes
// })


const router= createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const userole=localStorage.getItem('userole')
    console.log(userole)
    
    if (to.meta.isAdmin && userole!='admin'){
        next({ path: '/login',query: { unauthorized: true } })
    }else{
        next()

    }
        

});


export default router;