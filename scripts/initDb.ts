import { Client } from 'pg'
import dotenv from 'dotenv'
import fs from 'fs'
import path from 'path'

dotenv.config()

const client = new Client({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  ssl: { rejectUnauthorized: false }
})

async function initDb() {
  try {
    console.log('Connecting to database...')
    await client.connect()
    console.log('Connected to database!')
    
    const schemaPath = path.join(__dirname, '../ops/schema.sql')
    const schemaSql = fs.readFileSync(schemaPath, 'utf8')
    
    console.log('Running schema migration...')
    await client.query(schemaSql)
    console.log('Database schema initialized successfully!')
  } catch (err) {
    console.error('Error initializing database:', err)
  } finally {
    await client.end()
  }
}

initDb()
