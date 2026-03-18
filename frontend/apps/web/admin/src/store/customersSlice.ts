import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getCustomersAPI, createCustomerAPI, updateCustomerAPI, deleteCustomerAPI } from '@/api/customers'

interface Customer {
  id: number
  name: string
  code: string
  type: string
  level: string
  contact: string
  phone: string
  status: string
}

interface CustomersState {
  customers: Customer[]
  isLoading: boolean
  error: string | null
}

const initialState: CustomersState = {
  customers: [],
  isLoading: false,
  error: null,
}

export const getCustomers = createAsyncThunk(
  'customers/getCustomers',
  async (_, { rejectWithValue }) => {
    try {
      const response = await getCustomersAPI()
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const createCustomer = createAsyncThunk(
  'customers/createCustomer',
  async (customer: Omit<Customer, 'id'>, { rejectWithValue }) => {
    try {
      const response = await createCustomerAPI(customer)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const updateCustomer = createAsyncThunk(
  'customers/updateCustomer',
  async (customer: Customer, { rejectWithValue }) => {
    try {
      const response = await updateCustomerAPI(customer.id, customer)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const deleteCustomer = createAsyncThunk(
  'customers/deleteCustomer',
  async (customerId: number, { rejectWithValue }) => {
    try {
      await deleteCustomerAPI(customerId)
      return customerId
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

const customersSlice = createSlice({
  name: 'customers',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getCustomers.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(getCustomers.fulfilled, (state, action) => {
        state.isLoading = false
        state.customers = action.payload
      })
      .addCase(getCustomers.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(createCustomer.fulfilled, (state, action) => {
        state.customers.push(action.payload)
      })
      .addCase(updateCustomer.fulfilled, (state, action) => {
        const index = state.customers.findIndex(c => c.id === action.payload.id)
        if (index !== -1) {
          state.customers[index] = action.payload
        }
      })
      .addCase(deleteCustomer.fulfilled, (state, action) => {
        state.customers = state.customers.filter(c => c.id !== action.payload)
      })
  },
})

export default customersSlice.reducer