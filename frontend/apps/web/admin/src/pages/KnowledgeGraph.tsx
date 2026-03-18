import { useEffect, useState } from 'react'
import { Card, Row, Col, Button, Input, Select } from 'antd'
import { SearchOutlined, ReloadOutlined, DownloadOutlined } from '@ant-design/icons'

const { Option } = Select

const KnowledgeGraph = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState('product')

  const handleSearch = () => {
    console.log('搜索:', searchQuery, '类型:', searchType)
  }

  return (
    <div>
      <h2>知识图谱</h2>
      
      <div style={{ display: 'flex', marginBottom: 24, gap: 16 }}>
        <Input 
          placeholder="搜索关键词" 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ flex: 1 }}
        />
        <Select 
          value={searchType}
          onChange={setSearchType}
          style={{ width: 120 }}
        >
          <Option value="product">商品</Option>
          <Option value="customer">客户</Option>
          <Option value="category">分类</Option>
        </Select>
        <Button type="primary" icon={<SearchOutlined />} onClick={handleSearch}>搜索</Button>
        <Button icon={<ReloadOutlined />}>刷新</Button>
        <Button icon={<DownloadOutlined />}>导出</Button>
      </div>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="商品关联图谱" variant="outlined" style={{ height: 500 }}>
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <p>商品关联图谱可视化</p>
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="客户购买行为分析" variant="outlined" style={{ height: 500 }}>
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <p>客户购买行为分析可视化</p>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={12}>
          <Card title="智能推荐结果" variant="outlined" style={{ height: 300 }}>
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <p>基于知识图谱的智能推荐结果</p>
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="语义搜索结果" variant="outlined" style={{ height: 300 }}>
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <p>基于知识图谱的语义搜索结果</p>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export { KnowledgeGraph }