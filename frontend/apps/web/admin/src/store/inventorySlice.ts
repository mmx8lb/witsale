import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getInventoryAPI, updateInventoryAPI } from '@/api/inventory'

interface Inventory {
  id: number
  product_id: number
  product_name: string
  warehouse_id: number
  warehouse_name: string
  quantity: number
  status: string
}

interface InventoryState {
  inventory: Inventory[]
  isLoading: boolean
  error: string | null
}

const initialState: InventoryState = {
  inventory: [],
  isLoading: false,
  error: null,
}

export const getInventory = createAsyncThunk(
  'inventory/getInventory',
  async (_, { rejectWithValue }) => {
    try {
      const response = await getInventoryAPI()
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const updateInventory = createAsyncThunk(
  'inventory/updateInventory',
  async (inventory: Inventory, { rejectWithValue }) => {
    try {
      const response = await updateInventoryAPI(inventory.id, inventory)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

const inventorySlice = createSlice({
  name: 'inventory',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getInventory.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(getInventory.fulfilled, (state, action) => {
        state.isLoading = false
        state.inventory = action.payload
      })
      .addCase(getInventory.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(updateInventory.fulfilled, (state, action) => {
        const index = state.inventory.findIndex(i => i.id === action.payload.id)
        if (index !== -1) {
          state.inventory[index] = action.payload
        }
      })
  },
})

export default inventorySlice.reducer