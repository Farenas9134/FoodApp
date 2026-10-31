import { useEffect, useState } from "react";

// delay = 500ms (half a second)
const useDebounce = (value: string, delay = 500) => {
    const [ debouncedValue, setDebouncedValue ] = useState(value)

    useEffect(() => {
        const id = setTimeout(() => {
            // console.log(`setting new timeout: id-${id}`)
            setDebouncedValue(value)
        }, delay)

        return () => {
            // console.log(`clearing the timeout: id-${id}`)
            clearTimeout(id)
        }
    }, [value, delay])
    return (
        debouncedValue
    )
}
export default useDebounce