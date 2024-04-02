'use client';
 
// import { useParams } from 'next/navigation';
 
export default function AddSourceLayout({children}) {
  // const params = useParams<{ id }>()
 
  // Route -> /shop/[tag]/[item]
  // URL -> /shop/shoes/nike-air-max-97
  // `params` -> { tag: 'shoes', item: 'nike-air-max-97' }
 
  return (
    <main>
      <span>
        Hello Add Sources
      </span>
      {children}
    </main>
  );
}
