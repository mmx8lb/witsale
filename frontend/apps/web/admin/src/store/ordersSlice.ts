import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getOrdersAPI, updateOrderStatusAPI } from '@/api/orders'

interface Order {
  id: number
  order_no: string
  customer_id: number
  customer_name: string
  amount: number
  status: string
  created_at: string
}

interface OrdersState {
  orders: Order[]
  isLoading: boolean
  error: string | null
}

const initialState: OrdersState = {
  orders: [],
  isLoading: false,
  error: null,
}

export const getOrders = createAsyncThunk(
  'orders/getOrders',
  async (_, { rejectWithValue }) => {
    try {
      const response = await getOrdersAPI()
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const updateOrderStatus = createAsyncThunk(
  'orders/updateOrderStatus',
  async ({ orderId, status }: { orderId: number; status: string }, { rejectWithValue }) => {
    try {
      const response = await updateOrderStatusAPI(orderId, status)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

const ordersSlice = createSlice({
  name: 'orders',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getOrders.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(getOrders.fulfilled, (state, action) => {
        state.isLoading = false
        state.orders = action.payload
      })
      .addCase(getOrders.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(updateOrderStatus.fulfilled, (state, action) => {
        const index = state.orders.findIndex(o => o.id === action.payload.id)
        if (index !== -1) {
          state.orders[index] = action.payload
        }
      })
  },
})

export default ordersSlice.reducer