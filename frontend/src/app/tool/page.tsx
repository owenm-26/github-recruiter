"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

import Header from "@/components/layout/Header"
import Footer from "@/components/layout/Footer"
import { Button } from "@/components/ui/button"
import { Loader2Icon } from "lucide-react"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"

// Regular expression to validate a GitHub user profile URL
const githubUrlRegex = /^https?:\/\/github\.com\/[a-zA-Z0-9-]{1,39}$/

const formSchema = z.object({
  githubUrl: z
    .string()
    .regex(githubUrlRegex, {
      message: "Please enter a valid GitHub user URL (e.g., https://github.com/abc123)",
    }),
  jobDescription: z.string().min(1, {
    message: "Job Description is required.",
  }),
})

export default function ToolPage() {
  const [submitted, setSubmitted] = useState<boolean>(false)
  const [loading, setLoading] = useState<boolean>(false)
  const [results, setResults] = useState<string | null>(null)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      githubUrl: "",
      jobDescription: "",
    },
  })

  const handleSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      setLoading(true)
      // Replace with API Call
      await new Promise((resolve) => setTimeout(resolve, 1500))
      setResults("Success!")
      setSubmitted(true)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <Header />

      {submitted ? (
        <div className="text-center space-y-8">
          <h2 className="text-2xl font-bold">{results}</h2>
          <Button
            variant="default"
            onClick={() => {
              setSubmitted(false)
              form.reset()
            }}
          >
            Submit Another
          </Button>
        </div>
      ) : (
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className="text-center space-y-8 w-full max-w-md"
          >
            <FormField
              control={form.control}
              name="githubUrl"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Github URL</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter Github URL" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="jobDescription"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Job Description</FormLabel>
                  <FormControl>
                    <Textarea placeholder="Job Description" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button type="submit" disabled={loading} className="w-full">
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <Loader2Icon className="h-4 w-4 animate-spin" />
                  Submitting...
                </span>
              ) : (
                "Submit"
              )}
            </Button>
          </form>
        </Form>
      )}

      <Footer />
    </div>
  )
}