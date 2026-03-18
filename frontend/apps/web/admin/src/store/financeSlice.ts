import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getAccountsAPI, getTransactionsAPI, getInvoicesAPI, generateReportAPI } from '@/api/finance'

interface Account {
  id: number
  name: string
  code: string
  type: string
  balance: number
  currency: string
  status: string
}

interface Transaction {
  id: number
  transaction_no: string
  account_id: number
  type: string
  amount: number
  currency: string
  status: string
  payment_method: string
  created_at: string
}

interface Invoice {
  id: number
  invoice_no: string
  account_id: number
  amount: number
  currency: string
  status: string
  issue_date: string
  total_amount: number
}

interface FinanceState {
  accounts: Account[]
  transactions: Transaction[]
  invoices: Invoice[]
  reports: any[]
  isLoading: boolean
  error: string | null
}

const initialState: FinanceState = {
  accounts: [],
  transactions: [],
  invoices: [],
  reports: [],
  isLoading: false,
  error: null,
}

export const getAccounts = createAsyncThunk(
  'finance/getAccounts',
  async (_, { rejectWithValue }) => {
    try {
      const response = await getAccountsAPI()
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const getTransactions = createAsyncThunk(
  'finance/getTransactions',
  async (_, { rejectWithValue }) => {
    try {
      const response = await getTransactionsAPI()
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const getInvoices = createAsyncThunk(
  'finance/getInvoices',
  async (_, { rejectWithValue }) => {
    try {
      const response = await getInvoicesAPI()
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const generateReport = createAsyncThunk(
  'finance/generateReport',
  async (params: { startDate: string; endDate: string }, { rejectWithValue }) => {
    try {
      const response = await generateReportAPI(params)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

const financeSlice = createSlice({
  name: 'finance',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getAccounts.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(getAccounts.fulfilled, (state, action) => {
        state.isLoading = false
        state.accounts = action.payload
      })
      .addCase(getAccounts.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(getTransactions.fulfilled, (state, action) => {
        state.transactions = action.payload
      })
      .addCase(getInvoices.fulfilled, (state, action) => {
        state.invoices = action.payload
      })
      .addCase(generateReport.fulfilled, (state, action) => {
        state.reports.push(action.payload)
      })
  },
})

export default financeSlice.reducer