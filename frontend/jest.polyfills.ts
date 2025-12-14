import { TextEncoder, TextDecoder } from 'util'
import { ReadableStream, WritableStream, TransformStream } from 'stream/web'
import { BroadcastChannel } from 'worker_threads'

Object.assign(global, { 
  TextEncoder, 
  TextDecoder,
  ReadableStream,
  WritableStream,
  TransformStream,
  BroadcastChannel
})
