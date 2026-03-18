import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Table, Button, DatePicker, Tabs, message } from 'antd'
import { DollarOutlined, TransactionOutlined, FileTextOutlined, BarChartOutlined } from '@ant-design/icons'
import { getAccounts, getTransactions, getInvoices, generateReport } from '@/store/financeSlice'

const { TabPane } = Tabs
const { RangePicker } = DatePicker

const Finance = () => {
  const dispatch = useDispatch()
  const { accounts, transactions, invoices, reports, isLoading, error } = useSelector((state: any) => state.finance)
  const [dateRange, setDateRange] = useState<[any, any]>([null, null])

  useEffect(() => {
    dispatch(getAccounts())
    dispatch(getTransactions())
    dispatch(getInvoices())
  }, [dispatch])

  const handleGenerateReport = async () => {
    if (!dateRange[0] || !dateRange[1]) {
      message.error('请选择日期范围')
      return
    }
    try {
      await dispatch(generateReport({
        startDate: dateRange[0].format('YYYY-MM-DD'),
        endDate: dateRange[1].format('YYYY-MM-DD')
      })).unwrap()
      message.success('报表生成成功')
    } catch (err) {
      message.error('报表生成失败')
    }
  }

  const accountColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '账户名称', dataIndex: 'name', key: 'name' },
    { title: '账户编码', dataIndex: 'code', key: 'code' },
    { title: '账户类型', dataIndex: 'type', key: 'type' },
    { title: '余额', dataIndex: 'balance', key: 'balance', render: (balance: number) => `¥${balance}` },
    { title: '货币', dataIndex: 'currency', key: 'currency' },
    { title: '状态', dataIndex: 'status', key: 'status' },
  ]

  const transactionColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '交易编号', dataIndex: 'transaction_no', key: 'transaction_no' },
    { title: '账户ID', dataIndex: 'account_id', key: 'account_id' },
    { title: '交易类型', dataIndex: 'type', key: 'type' },
    { title: '金额', dataIndex: 'amount', key: 'amount', render: (amount: number) => `¥${amount}` },
    { title: '货币', dataIndex: 'currency', key: 'currency' },
    { title: '状态', dataIndex: 'status', key: 'status' },
    { title: '支付方式', dataIndex: 'payment_method', key: 'payment_method' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
  ]

  const invoiceColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '发票编号', dataIndex: 'invoice_no', key: 'invoice_no' },
    { title: '账户ID', dataIndex: 'account_id', key: 'account_id' },
    { title: '金额', dataIndex: 'amount', key: 'amount', render: (amount: number) => `¥${amount}` },
    { title: '货币', dataIndex: 'currency', key: 'currency' },
    { title: '状态', dataIndex: 'status', key: 'status' },
    { title: '开票日期', dataIndex: 'issue_date', key: 'issue_date' },
    { title: '总金额', dataIndex: 'total_amount', key: 'total_amount', render: (amount: number) => `¥${amount}` },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2>财务管理</h2>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <RangePicker style={{ marginRight: 16 }} onChange={(dates) => setDateRange(dates as [any, any])} />
          <Button type="primary" icon={<BarChartOutlined />} onClick={handleGenerateReport}>生成报表</Button>
        </div>
      </div>
      
      <Tabs defaultActiveKey="accounts">
        <TabPane tab={<><DollarOutlined /> 账户管理</>} key="accounts">
          <Table 
            columns={accountColumns} 
            dataSource={accounts} 
            rowKey="id" 
            loading={isLoading}
            pagination={{ pageSize: 10 }}
          />
        </TabPane>
        <TabPane tab={<><TransactionOutlined /> 交易管理</>} key="transactions">
          <Table 
            columns={transactionColumns} 
            dataSource={transactions} 
            rowKey="id" 
            loading={isLoading}
            pagination={{ pageSize: 10 }}
          />
        </TabPane>
        <TabPane tab={<><FileTextOutlined /> 发票管理</>} key="invoices">
          <Table 
            columns={invoiceColumns} 
            dataSource={invoices} 
            rowKey="id" 
            loading={isLoading}
            pagination={{ pageSize: 10 }}
          />
        </TabPane>
      </Tabs>
    </div>
  )
}

export { Finance }