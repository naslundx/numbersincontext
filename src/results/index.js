import useSearch from "../hooks/useSearch"
import ResultItem from "./ResultItem";
import "./results.css"

const Results = ({ searchTerms }) => {
    const searchResults = useSearch(searchTerms);

    return (
        <div className="result transparentbox">
            {searchResults.map(e => <ResultItem data={e} />)}
            {searchResults.length === 0 && <p>Enter a number...</p>}
        </div>
    )
}

export default Results;