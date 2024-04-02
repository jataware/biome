'use client';
 
import { useParams } from 'next/navigation';
 
export default function SourceLayout({children}) {
  const params = useParams<{ id }>()
 
  // Route -> /shop/[tag]/[item]
  // URL -> /shop/shoes/nike-air-max-97
  // `params` -> { tag: 'shoes', item: 'nike-air-max-97' }
  console.log(params);
 
  return (
    <main>
      <span>
        Hello Source Page
      </span>
      {children}
    </main>
  );
}
