"use client"

import { useState } from "react"
import Header from "@/components/layout/Header"
import Footer from "@/components/layout/Footer"
import { Button, Input, Form } from "antd"
import { SyncOutlined } from "@ant-design/icons"

export default function ToolPage() {
    // SET TYPE FOR FORM
  const [form] = Form.useForm()
  const [submitted, setSubmitted] = useState<boolean>(false)
  const [loading, setLoading] = useState<boolean>(false)
  const [results, setResults] = useState<string | null>(null)

  const handleSubmit = async (values: { githubUrl: string; jobDescription: string }) => {
    try {
      setLoading(true) // start loading
      // Replace with API Call
      await new Promise((resolve) => setTimeout(resolve, 1500))
    //   Set results from API Call here 
      setResults("Success!")
      setSubmitted(true) // mark submission as complete
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false) // stop loading
    }
  }

  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <Header />

      {submitted ? (
        <div className="text-center space-y-8">
          <h2 className="text-2xl font-bold">{results}</h2>
          <Button type="primary" onClick={() => { setSubmitted(false); form.resetFields() }}>
            Submit Another
          </Button>
        </div>
      ) : (
        <Form
          form={form}
          onFinish={handleSubmit}
          className="text-center space-y-8 w-full max-w-md"
          layout="vertical"
        >
          <Form.Item
            name="githubUrl"
            rules={[{ required: true, message: "Github URL is required" }]}
          >
            <Input placeholder="Github URL" />
          </Form.Item>

          <Form.Item
            name="jobDescription"
            rules={[{ required: true, message: "Job Description is required" }]}
          >
            <Input placeholder="Job Description" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              icon={loading ? <SyncOutlined spin /> : undefined}
            >
              {loading ? "Submitting..." : "Submit"}
            </Button>
          </Form.Item>
        </Form>
      )}

      <Footer />
    </div>
  )
}
