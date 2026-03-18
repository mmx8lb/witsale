import { configureStore } from '@reduxjs/toolkit'
import authReducer from './authSlice'
import productsReducer from './productsSlice'
import ordersReducer from './ordersSlice'
import inventoryReducer from './inventorySlice'
import customersReducer from './customersSlice'
import financeReducer from './financeSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    products: productsReducer,
    orders: ordersReducer,
    inventory: inventoryReducer,
    customers: customersReducer,
    finance: financeReducer,
  },
})