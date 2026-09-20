        """Minimal Seedream example: create one prediction and print the output URL(s)."""
        import seedream_api

        output = seedream_api.run({
    "prompt": "Replace the sky with a dramatic sunset, keep everything else exactly as it is",
    "image_urls": [
        "https://example.com/input.png"
    ]
})
        print(output)
