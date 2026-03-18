import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getProductsAPI, createProductAPI, updateProductAPI, deleteProductAPI } from '@/api/products'

interface Product {
  id: number
  name: string
  code: string
  price: number
  stock: number
  status: string
}

interface ProductsState {
  products: Product[]
  isLoading: boolean
  error: string | null
}

const initialState: ProductsState = {
  products: [],
  isLoading: false,
  error: null,
}

export const getProducts = createAsyncThunk(
  'products/getProducts',
  async (_, { rejectWithValue }) => {
    try {
      const response = await getProductsAPI()
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const createProduct = createAsyncThunk(
  'products/createProduct',
  async (product: Omit<Product, 'id'>, { rejectWithValue }) => {
    try {
      const response = await createProductAPI(product)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const updateProduct = createAsyncThunk(
  'products/updateProduct',
  async (product: Product, { rejectWithValue }) => {
    try {
      const response = await updateProductAPI(product.id, product)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const deleteProduct = createAsyncThunk(
  'products/deleteProduct',
  async (productId: number, { rejectWithValue }) => {
    try {
      await deleteProductAPI(productId)
      return productId
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

const productsSlice = createSlice({
  name: 'products',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getProducts.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(getProducts.fulfilled, (state, action) => {
        state.isLoading = false
        state.products = action.payload
      })
      .addCase(getProducts.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(createProduct.fulfilled, (state, action) => {
        state.products.push(action.payload)
      })
      .addCase(updateProduct.fulfilled, (state, action) => {
        const index = state.products.findIndex(p => p.id === action.payload.id)
        if (index !== -1) {
          state.products[index] = action.payload
        }
      })
      .addCase(deleteProduct.fulfilled, (state, action) => {
        state.products = state.products.filter(p => p.id !== action.payload)
      })
  },
})

export default productsSlice.reducer